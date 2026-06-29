#!/usr/bin/env python3
"""SessionStart telemetry for the Testery Claude Code plugin (TESTERY-1768).

Emits a `plugin_session_started` event to PostHog so we can detect that the
plugin is installed and in use. This is the practical proxy for "installed":
Claude Code plugins have no install-time hook, so the first time the plugin is
active in a session is the earliest signal we can capture.

Design constraints:
* Runs in the *user's* Python, where `requests` may not exist -> stdlib only.
* Strictly best-effort: never raises, never prints to stdout (SessionStart stdout
  would be injected into the model's context), short network timeout.
* Shares ~/.testery/anonymous_id with the CLI so plugin and CLI events correlate.
"""
import json
import os
import platform
import sys
import urllib.request
import uuid
from pathlib import Path

# Same public, write-only PostHog project ingest key the CLI ships. Not a secret.
DEFAULT_POSTHOG_KEY = 'phc_m5DpsXorttoodLH5US5VzwPRDDjuNFrCfeim3NQoo6gk'
DEFAULT_POSTHOG_HOST = 'https://us.i.posthog.com'

ANON_ID_PATH = Path.home() / '.testery' / 'anonymous_id'
TIMEOUT_SECONDS = 1.5

_OFF_VALUES = {'0', 'false', 'no', 'off'}
_ON_VALUES = {'1', 'true', 'yes', 'on'}


def _enabled():
    if os.environ.get('DO_NOT_TRACK', '').strip().lower() in _ON_VALUES:
        return False
    flag = os.environ.get('TESTERY_TELEMETRY')
    if flag is not None and flag.strip().lower() in _OFF_VALUES:
        return False
    return True


def _anonymous_id():
    try:
        if ANON_ID_PATH.exists():
            existing = ANON_ID_PATH.read_text().strip()
            if existing:
                return existing
    except OSError:
        pass
    new_id = str(uuid.uuid4())
    try:
        ANON_ID_PATH.parent.mkdir(parents=True, exist_ok=True)
        ANON_ID_PATH.write_text(new_id)
        try:
            os.chmod(ANON_ID_PATH, 0o600)
        except OSError:
            pass
    except OSError:
        pass
    return new_id


def _plugin_version():
    root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if not root:
        return 'unknown'
    try:
        meta = json.loads((Path(root) / '.claude-plugin' / 'plugin.json').read_text())
        return meta.get('version', 'unknown')
    except Exception:
        return 'unknown'


def _session_source():
    """Claude passes JSON on stdin with a `source` like startup/resume/clear."""
    try:
        payload = json.loads(sys.stdin.read() or '{}')
        return payload.get('source')
    except Exception:
        return None


def main():
    if not _enabled():
        return
    try:
        host = (os.environ.get('TESTERY_POSTHOG_HOST') or DEFAULT_POSTHOG_HOST).rstrip('/')
        body = json.dumps({
            'api_key': os.environ.get('TESTERY_POSTHOG_KEY') or DEFAULT_POSTHOG_KEY,
            'event': 'plugin_session_started',
            'distinct_id': _anonymous_id(),
            'properties': {
                'source': 'claude-plugin',
                'plugin_version': _plugin_version(),
                'session_source': _session_source(),
                'ci': bool(os.environ.get('CI')),
                'os': platform.system(),
                'os_release': platform.release(),
                'python_version': platform.python_version(),
            },
        }).encode('utf-8')
        req = urllib.request.Request(
            host + '/capture/', data=body,
            headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS).close()
    except Exception:
        pass


if __name__ == '__main__':
    main()
