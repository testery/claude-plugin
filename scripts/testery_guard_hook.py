#!/usr/bin/env python3
"""PreToolUse guard. If a Bash command runs the `testery` CLI but the CLI is not
installed, or is installed but not yet onboarded (no saved token), block the call
and tell the model to run the matching setup flow.

Written in Python so one file behaves identically on Windows, macOS, and Linux.
FAILS OPEN: any unexpected error allows the command, so a broken hook can never
brick the user's Bash tool. Auth subcommands (login/verify-token/help/version) are
never blocked, so the onboarding flow itself can run.
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

WELCOME = "Your AI-enabled testing journey with Testery is about to begin! \U0001F916"

NOT_INSTALLED_REASON = (
    "The Testery CLI is not installed, so this command would fail. Do NOT retry it yet. "
    "First, display this message to the user exactly:\n\n"
    f"{WELCOME}\n\n"
    "Then use the AskUserQuestion tool to ask a yes/no question about installing the "
    "Testery CLI (it unlocks running tests on Testery's cloud, live monitoring, schedules, "
    "environments, and more). If they say yes, install it (`python3 -m pip install testery`, "
    "or `python -m pip install testery`, or `pipx install testery`) and then retry. If they "
    "say no, tell them Testery commands won't work until it's installed and do not re-ask "
    "this session. See the testery-cli-setup skill."
)

NOT_ONBOARDED_REASON = (
    "The Testery CLI is installed but not yet authenticated (no saved token / credentials). "
    "Do NOT retry this command yet. Run the testery-onboard skill to sign in — it walks the "
    "user through signup or pasting an API token and saves credentials. Once onboarding "
    "completes (a token is saved or $TESTERY_API_TOKEN is set), retry the command."
)

# Subcommands that must run even when not installed/onboarded (they ARE onboarding).
ALLOW_SUBCOMMANDS = {"login", "verify-token", "help", "version"}

_SEP = re.compile(r"[;\n|&()]+")
_ENV_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def testery_subcommand(command):
    """If `testery` is run as a program, return its first subcommand ('' if none);
    return None if the command does not invoke testery."""
    for segment in _SEP.split(command):
        tokens = segment.strip().split()
        i = 0
        while i < len(tokens) and _ENV_ASSIGN.match(tokens[i]):  # skip VAR=val prefixes
            i += 1
        if i < len(tokens) and tokens[i] == "testery":
            rest = tokens[i + 1:]
            return rest[0] if rest else ""
    return None


def onboarded():
    if os.environ.get("TESTERY_API_TOKEN"):
        return True
    creds = Path.home() / ".testery" / "credentials"
    try:
        return creds.is_file() and creds.stat().st_size > 0
    except OSError:
        return False


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return  # fail open
    if data.get("tool_name") != "Bash":
        return
    command = (data.get("tool_input") or {}).get("command", "")
    sub = testery_subcommand(command)
    if sub is None:
        return  # not a testery invocation
    # Never block onboarding/help/version, or bare `testery` / flag-only invocations.
    if sub == "" or sub.startswith("-") or sub in ALLOW_SUBCOMMANDS:
        return
    if not shutil.which("testery"):
        deny(NOT_INSTALLED_REASON)
        return
    if not onboarded():
        deny(NOT_ONBOARDED_REASON)
        return
    # READY -> allow


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # fail open
    sys.exit(0)
