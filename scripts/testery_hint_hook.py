#!/usr/bin/env python3
"""PostToolUse hook: relay a Testery CLI hint into the Claude session (TESTERY-1774).

The `testery` CLI, when driven from this plugin, may print one line on stderr after
its result:

    testery-hint: {"hint": "ci-gating", "source": "claude-plugin", "surface": "list-test-runs", ...}

Claude already sees that line in the Bash tool result, but a bare stderr line is easy
to drop or, worse, to lead with. This hook finds it and hands Claude explicit
`additionalContext`: present the command's result first, then the hint as ONE footer
line, at most once per session. It also records a `hint_relayed` telemetry event with
the same source/surface/hint attribution, so we can see the hint made it into a
session (the CLI records `hint_emitted` on its side).

Constraints, same as the other plugin hooks:
* stdlib only (the user's Python may not have `requests`),
* never raises, never blocks the tool call, prints nothing unless there is a hint,
* `TESTERY_HINTS=0` silences relaying, `TESTERY_TELEMETRY=0` / `DO_NOT_TRACK` silence
  the event.
"""
import json
import os
import re
import sys
import urllib.request

# Reuse the SessionStart telemetry helpers (same anon id, key, opt-outs).
from testery_telemetry import (DEFAULT_POSTHOG_HOST, DEFAULT_POSTHOG_KEY, TIMEOUT_SECONDS,
                               _anonymous_id, _enabled, _plugin_version)

SENTINEL = 'testery-hint:'
_OFF_VALUES = {'0', 'false', 'no', 'off'}
# `testery` as a command word, not as part of a path/word like "testery-cli/".
_TESTERY_CMD = re.compile(r'(^|[\s;&|(=])testery(\.exe)?\s')


def _texts(value):
    """Every string inside the tool response (shape varies across Claude Code versions)."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _texts(v)
    elif isinstance(value, list):
        for v in value:
            yield from _texts(v)


def find_hint(tool_response):
    for text in _texts(tool_response):
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith(SENTINEL):
                continue
            try:
                hint = json.loads(line[len(SENTINEL):])
            except ValueError:
                continue
            if isinstance(hint, dict) and hint.get('hint') and hint.get('message'):
                return hint
    return None


def relay_instructions(hint):
    attribution = 'source=%s surface=%s hint=%s' % (
        hint.get('source'), hint.get('surface'), hint.get('hint'))
    tip = hint['message']
    if hint.get('action'):
        tip += ' ' + hint['action']
    return (
        'Testery hint from the CLI (%s): "%s"\n'
        'How to relay it: first give the user the result of the command they asked for, '
        'complete and unchanged in priority. Then end your reply with this hint as ONE '
        'line starting with "💡 Testery tip:", keeping the link exactly as written '
        '(its query string is the attribution). Do not lead with it, do not expand on '
        'it, and do not show the same hint again this session. Skip it if the user has '
        'asked not to see tips.' % (attribution, tip)
    )


def _record(hint, session_id):
    if not _enabled():
        return
    try:
        host = (os.environ.get('TESTERY_POSTHOG_HOST') or DEFAULT_POSTHOG_HOST).rstrip('/')
        body = json.dumps({
            'api_key': os.environ.get('TESTERY_POSTHOG_KEY') or DEFAULT_POSTHOG_KEY,
            'event': 'hint_relayed',
            'distinct_id': _anonymous_id(),
            'properties': {
                'source': hint.get('source') or 'claude-plugin',
                'surface': hint.get('surface'),
                'hint': hint.get('hint'),
                'plugin_version': _plugin_version(),
                'claude_session_id': session_id,
            },
        }).encode('utf-8')
        req = urllib.request.Request(host + '/capture/', data=body,
                                     headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS).close()
    except Exception:
        pass


def main():
    try:
        flag = os.environ.get('TESTERY_HINTS')
        if flag is not None and flag.strip().lower() in _OFF_VALUES:
            return
        payload = json.loads(sys.stdin.read() or '{}')
        # Claude Code on Windows may run the CLI through its PowerShell tool instead of Bash.
        if payload.get('tool_name') not in ('Bash', 'PowerShell'):
            return
        command = (payload.get('tool_input') or {}).get('command') or ''
        if not _TESTERY_CMD.search(' ' + command + ' '):
            return
        hint = find_hint(payload.get('tool_response'))
        if hint is None:
            return
        sys.stdout.write(json.dumps({
            'hookSpecificOutput': {
                'hookEventName': 'PostToolUse',
                'additionalContext': relay_instructions(hint),
            }
        }))
        sys.stdout.flush()
        _record(hint, payload.get('session_id'))
    except Exception:
        return


if __name__ == '__main__':
    main()
