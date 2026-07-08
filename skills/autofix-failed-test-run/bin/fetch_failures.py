#!/usr/bin/env python3
"""Fetch a Testery test run's failures as a compact diagnostic bundle.

Used by the `autofix-failed-test-run` skill. Stdlib only (no `requests`), so it
runs anywhere Python 3 does, on Windows / macOS / Linux, with no extra install.

Auth + API resolution mirror the `testery` CLI:
  token   : --token > $TESTERY_API_TOKEN > [profile].token in ~/.testery/credentials
  api base: --api-url > $TESTERY_API_URL > https://api.testery.io/api  (dev: --dev)

The run is resolved from --test-run-id, a full run URL, or --latest (the most
recent run for the authenticated account). Everything is scoped to the token's
account, so a partner running this with their own token sees only their runs.

Output: a single JSON object on stdout with the account, the run summary, and one
entry per FAILED test (name, file, trimmed error, a tail of the runner output,
and screenshot/video URLs). Diagnosis and any fixes are left to the agent.
"""
import argparse
import configparser
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_API = "https://api.testery.io/api"
DEV_API = "https://api.dev.testery.io/api"
CREDENTIALS_PATH = Path.home() / ".testery" / "credentials"

# Keep the bundle small enough to reason about without burning the context window.
ERROR_CHARS = 4000
OUTPUT_TAIL_CHARS = 4000
MAX_ARTIFACTS = 6


def resolve_token(explicit, profile):
    if explicit:
        return explicit
    if CREDENTIALS_PATH.exists():
        parser = configparser.ConfigParser()
        try:
            parser.read(CREDENTIALS_PATH)
            section = profile or "default"
            if parser.has_option(section, "token"):
                tok = parser.get(section, "token").strip()
                if tok:
                    return tok
        except configparser.Error:
            pass
    return os.environ.get("TESTERY_API_TOKEN")


def api_get(api_url, token, path):
    """GET {api_url}{path} with the bearer token. Returns parsed JSON or raises."""
    req = urllib.request.Request(
        api_url + path,
        headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8", "replace")
    return json.loads(body) if body.strip() else None


def parse_run_id(value):
    """Accept a bare id or a testery.app run URL and return the numeric id string."""
    if not value:
        return None
    value = value.strip()
    if value.isdigit():
        return value
    m = re.search(r"/test-runs/(\d+)", value)
    if m:
        return m.group(1)
    m = re.search(r"(\d+)", value)
    return m.group(1) if m else None


def latest_run_id(api_url, token):
    runs = api_get(api_url, token, "/test-runs?limit=1&offset=0") or []
    if not runs:
        return None
    return str(runs[0].get("id"))


def trim(text, limit):
    text = text or ""
    if len(text) <= limit:
        return text
    return text[:limit] + "\n... [truncated %d chars]" % (len(text) - limit)


def tail(text, limit):
    text = text or ""
    if len(text) <= limit:
        return text
    return "... [truncated %d chars]\n" % (len(text) - limit) + text[-limit:]


def main():
    ap = argparse.ArgumentParser(description="Fetch a Testery run's failures.")
    ap.add_argument("run", nargs="?", help="Test run id or run URL (omit with --latest).")
    ap.add_argument("--test-run-id", dest="run_id", help="Test run id (alternative to positional).")
    ap.add_argument("--latest", action="store_true", help="Use the account's most recent run.")
    ap.add_argument("--token", help="Testery API token (else env/credentials).")
    ap.add_argument("--profile", help="Credentials profile (default: default).")
    ap.add_argument("--api-url", help="API base URL override.")
    ap.add_argument("--dev", action="store_true", help="Target the Testery dev API.")
    args = ap.parse_args()

    token = resolve_token(args.token, args.profile)
    if not token:
        json.dump({"error": "no_token",
                   "message": "No Testery token found. Run the testery-onboard skill, "
                              "set TESTERY_API_TOKEN, or pass --token."},
                  sys.stdout)
        return 3

    api_url = args.api_url or os.environ.get("TESTERY_API_URL") or (DEV_API if args.dev else DEFAULT_API)

    # Confirm the token is valid and capture *which* account we're acting on.
    try:
        account = api_get(api_url, token, "/account")
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            json.dump({"error": "unauthenticated",
                       "message": "Token was rejected (%s). Run the testery-onboard skill." % e.code},
                      sys.stdout)
            return 4
        raise
    account_summary = {
        "id": (account or {}).get("id"),
        "name": (account or {}).get("name"),
        "display": (account or {}).get("display"),
    }

    run_id = parse_run_id(args.run or args.run_id)
    if not run_id:
        if not args.latest and (args.run or args.run_id):
            json.dump({"error": "bad_run", "message": "Could not parse a run id from input."}, sys.stdout)
            return 2
        run_id = latest_run_id(api_url, token)
        if not run_id:
            json.dump({"error": "no_runs", "account": account_summary,
                       "message": "No test runs found for this account."}, sys.stdout)
            return 5

    try:
        run = api_get(api_url, token, "/test-runs/%s" % run_id) or {}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            json.dump({"error": "run_not_found", "account": account_summary, "run_id": run_id,
                       "message": "Run %s not found in this account." % run_id}, sys.stdout)
            return 6
        raise

    results = api_get(api_url, token, "/test-runs/%s/results" % run_id) or []
    failed = [r for r in results if (r.get("status") or "").upper() == "FAIL"]

    failures = []
    for r in failed:
        rid = r.get("id")
        detail = {}
        try:
            detail = api_get(api_url, token, "/test-runs/%s/results/%s" % (run_id, rid)) or {}
        except urllib.error.HTTPError:
            detail = {}
        pt = r.get("projectTest") or {}
        failures.append({
            "result_id": rid,
            "name": detail.get("name") or pt.get("name"),
            "file": detail.get("file") or pt.get("file"),
            "fileFilter": detail.get("fileFilter") or pt.get("fileFilter"),
            "status": r.get("status"),
            "durationMs": r.get("duration"),
            "error": trim(detail.get("error"), ERROR_CHARS),
            "stackTrace": trim(detail.get("stackTrace"), ERROR_CHARS),
            "outputTail": tail(detail.get("processOutput") or detail.get("output"), OUTPUT_TAIL_CHARS),
            "screenShots": (detail.get("screenShots") or [])[:MAX_ARTIFACTS],
            "videos": (detail.get("videos") or [])[:MAX_ARTIFACTS],
        })

    account_slug = account_summary.get("name") or account_summary.get("display")
    run_url = None
    if account_slug:
        run_url = "https://testery.app/%s/test-runs/%s" % (account_slug, run_id)

    bundle = {
        "account": account_summary,
        "run": {
            "id": run.get("id") or int(run_id) if str(run_id).isdigit() else run_id,
            "status": run.get("status"),
            "branch": run.get("branch"),
            "projectId": run.get("projectId"),
            "environmentId": run.get("environmentId"),
            "totalCount": run.get("totalCount"),
            "passCount": run.get("passCount"),
            "failCount": run.get("failCount"),
            "ignoredCount": run.get("ignoredCount"),
            "notRunCount": run.get("notRunCount"),
            "startTime": run.get("startTime"),
            "endTime": run.get("endTime"),
            "url": run_url,
        },
        "failureCount": len(failures),
        "failures": failures,
    }
    json.dump(bundle, sys.stdout, indent=2, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
