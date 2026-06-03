---
name: testery-create-deploy
description: Notify Testery that a deploy occurred for a project + environment. Triggers any deploy-type schedules attached to that environment. Use from CI after a deploy lands.
---

# Create a Testery deploy event

Wraps `testery create-deploy`.

```bash
testery create-deploy \
  --token "$TESTERY_TOKEN" \
  --project "<project-key>" \
  --environment "<env-key>" \
  [--commit <sha>] [--branch <name>] [--build-id <id>] \
  [--git-provider GitHub --git-owner <org> --git-repo <repo>] \
  [--wait-for-results --fail-on-failure --output pretty|json|teamcity]
```

`--wait-for-results` blocks until all triggered test runs finish.
