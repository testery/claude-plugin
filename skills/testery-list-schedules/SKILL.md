---
name: testery-list-schedules
description: List the Testery schedules (interval/cron and deploy triggers) configured for the account. Use when the user asks "what's scheduled?", "show me the test run schedules", "list schedules", or "/testery-list-schedules".
---

# List Testery schedules

Wraps `testery list-schedules`. Lists the schedules (triggers) configured for the account.

```bash
testery list-schedules \
  --token "$TESTERY_TOKEN" \
  [--show-archived] \
  [--output pretty|json]
```

Flags:
- `--show-archived`: include archived schedules in the output.
- `--output pretty|json`: output format (default `pretty`).
- Auth: `--token` / `--profile`, falling back to `~/.testery/credentials` or `$TESTERY_API_TOKEN`.

Prefer `--output json` when you need to read each schedule's fields (name, type, cron, project/environment) reliably; render a short per-schedule summary for the user otherwise.
