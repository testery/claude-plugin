---
name: testery-create-schedule
description: Create a Testery schedule that triggers test runs on a cron, on deploy, or following another run. Use when the user wants to "schedule tests", "run nightly", "trigger on deploy", etc.
---

# Create a Testery schedule

Wraps `testery create-schedule`. The `--schedule-type` is either `interval` (cron) or `deploy`.

## Common shapes

Interval (cron) — requires `--schedule-type interval` with `--cron`:
```bash
testery create-schedule \
  --token "$TESTERY_TOKEN" \
  --schedule-name "<name>" \
  --project-key "<project>" \
  --environment-key "<env>" \
  --schedule-type interval --cron "0 2 * * *" \
  [--git-branch main] [--include-tags @smoke] \
  [--runner-count 4] [--retry-failed-tests]
```

On deploy — `--schedule-type deploy`, optionally fired by another project's deploy:
```bash
testery create-schedule \
  --token "$TESTERY_TOKEN" \
  --schedule-name "<name>" \
  --project-key "<project>" \
  --environment-key "<env>" \
  --schedule-type deploy \
  [--on-deploy --deploy-project <key>] [--deploy-on-any-project] \
  [--include-tags @regression]
```

To get test-run event notifications from a schedule, add the `--follow-test-run` flag (it is a boolean flag, not a run id).

## Other useful flags

- `--build-id <id>` / `--git-ref <sha>`: pin to a specific build / commit (omit for "latest").
- `--run-specific-version`: run a specific version (used with `--git-branch`, `--build-id`, `--git-ref`) instead of latest.
- `--priority <n>`.
- `--copies <n>`, `--parallelize-by-file`, `--parallelize-by-test`.
- `--include-all-tags`: override testery.yml and run all available tags.
- `--variable KEY=VALUE` (repeatable; prefix `secure:` to encrypt).
- `--test-suite "Name"`.
- `--timeout-minutes`, `--test-timeout-seconds`, `--test-filter-regex`.
- `--on-deploy` + one or more `--deploy-project <key>`, or `--deploy-on-any-project`: trigger when another project deploys.
