---
description: Diagnose a failed Testery test run, then update the test, fix the bug, or file a bug report — one root cause at a time.
---

Use the `autofix-failed-test-run` skill.

`$ARGUMENTS` optionally contains a Testery test run id or run URL (e.g. `1010984` or
`https://testery.app/<account>/test-runs/1010984`). If no run is given, use the account's
**latest** test run.

Requires an authenticated Testery account: if the user is not logged in, run the
`testery-onboard` skill first, then continue.

User input (optional: test run id or URL): $ARGUMENTS
