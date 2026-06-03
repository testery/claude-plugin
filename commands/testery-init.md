---
description: Scaffold playwright-bdd tests in this project, register it on Testery, and run the first smoke.
---

Use the `testery-init` skill.

If the user isn't authenticated, route through `testery-onboard` first.

The skill is idempotent: it detects existing files, projects, and environments and skips/upserts rather than overwriting.

User input (e.g., desired project key or env name): $ARGUMENTS
