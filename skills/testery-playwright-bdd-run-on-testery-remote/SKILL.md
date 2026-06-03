---
name: testery-playwright-bdd-run-on-testery-remote
description: Run the REMOTE (Git-hosted) version of a playwright-bdd project on Testery, pinned to a branch or commit. Use when the user wants Testery to pull from Git and run.
---

# Run remote/Git version on Testery

```bash
testery create-test-run \
  --token "$TESTERY_TOKEN" \
  --project-key "<project>" \
  --environment-key "<env>" \
  --git-branch "<branch>"   # OR --git-ref "<sha>"
  [--include-tags @smoke] [--runner-count 4] \
  [--wait-for-results --fail-on-failure]
```

## Steps

1. Confirm with the user: branch (latest commit) vs specific commit SHA?
2. Confirm project + environment keys.
3. Run `create-test-run` with `--git-branch` or `--git-ref`.
4. Hand off to `testery-monitor-test-run` to follow.

For local working-copy code instead, use `testery-playwright-bdd-run-on-testery-local-build`.
