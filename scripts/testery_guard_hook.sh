#!/usr/bin/env bash
# Launcher for the PreToolUse guard. Finds a Python interpreter and execs the
# guard script, passing the hook's stdin JSON straight through.
#
# Why a launcher: hook commands run via sh on Unix and Git Bash on Windows, but
# the interpreter name varies (`python3` on macOS/Linux, often `python`/`py` on
# Windows). If no Python is found we exit 0 so the tool call proceeds (fail open).
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for py in python3 python py; do
  if command -v "$py" >/dev/null 2>&1; then
    exec "$py" "$DIR/testery_guard_hook.py"
  fi
done
exit 0
