---
description: Run a playwright-bdd project on Testery: local working copy or remote Git version.
---

Determine which version the user wants:

- **Local working copy**: use the `testery-playwright-bdd-run-on-testery-local-build` skill (zips the cwd, uploads, then creates a test run pinned to that build).
- **Remote Git version**: use the `testery-playwright-bdd-run-on-testery-remote` skill (creates a test run with `--git-branch` or `--git-ref`).

If the user has uncommitted changes or doesn't specify, ask which they want.

User input: $ARGUMENTS
