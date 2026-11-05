#!/usr/bin/env bash
# Launcher for the PostToolUse hint relay (TESTERY-1774). Finds a Python interpreter
# and execs the hook script, passing the hook's stdin JSON straight through.
# No Python -> exit 0 so the session proceeds (fail open), like the other hooks.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for py in python3 python py; do
  if command -v "$py" >/dev/null 2>&1; then
    exec "$py" "$DIR/testery_hint_hook.py"
  fi
done
exit 0
