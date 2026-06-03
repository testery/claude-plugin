# testery-claude-plugin

A [Claude Code](https://claude.ai/code) **plugin** for the [Testery](https://testery.io) test orchestration platform. Adds slash commands and skills that let Claude drive the entire Testery CLI surface (create test runs, upload artifacts, register environments, schedule runs, monitor progress, etc.) plus authoring helpers tailored to **playwright-bdd** projects.

## Install

This repo is a Claude Code plugin. From inside Claude Code:

```text
/plugin marketplace add testery/testery-skills
/plugin install testery@testery
```

That's it — Claude Code clones the repo, registers the marketplace, and installs the plugin. All `/testery-*` and `/bdd-*` commands and skills become available immediately.

### Alternative: install from a local clone

If you've already cloned this repo:

```text
/plugin marketplace add /absolute/path/to/testery-claude-plugin
/plugin install testery@testery
```

### Update / uninstall

```text
/plugin update testery@testery
/plugin uninstall testery@testery
/plugin marketplace remove testery
```

## Quickstart

After installing the plugin:

```text
/testery-onboard      # signup or login on testery.io, persist your API key
/testery-init         # scaffold playwright-bdd + register the project on Testery
```

`/testery-onboard` runs `testery login` (signing you up at `https://testery.app/signup` first if needed), which opens the API-keys page, captures your token, and saves it to `~/.testery/credentials` so it sticks across sessions. `/testery-init` scaffolds the project, runs a local smoke test, registers it on Testery, and (optionally) fires the first cloud run.

## What you get

### Slash commands

#### Testery platform

| Command | What it does |
|---|---|
| `/testery-onboard` | **Start here.** Sign up / log in, capture API key, persist it |
| `/testery-init` | Scaffold playwright-bdd in this project and wire it to Testery |
| `/testery-create-test-run` | Submit a Git-based test run |
| `/testery-monitor-test-run` | Follow a run to completion |
| `/testery-cancel-test-run` | Cancel a running test run |
| `/testery-list-active-test-runs` | Show in-flight runs |
| `/testery-list-test-runs` | List recent runs (filter by branch/status/etc.) |
| `/testery-report-test-run` | Output per-test results |
| `/testery-upload-artifacts` | Upload a local file/dir as a build |
| `/testery-add-file` | Attach a file to a test run |
| `/testery-register-environment` | Create a new environment |
| `/testery-update-environment` | Update an existing environment |
| `/testery-deregister-environment` | Delete an environment |
| `/testery-list-environments` | List environments |
| `/testery-upload-environment-file` | Upload a file to an env |
| `/testery-create-schedule` | Interval (cron) / on-deploy schedules |
| `/testery-list-schedules` | List configured schedules |
| `/testery-delete-schedule` | Remove a schedule |
| `/testery-create-deploy` | Notify Testery of a deploy |
| `/testery-create-alert` | Set up an alert |
| `/testery-run-test-plan` | Execute a saved test plan |
| `/testery-load-users` | Bulk-load users |
| `/testery-verify-token` | Auth health check |
| `/testery-run-playwright-bdd-local` | Run playwright-bdd tests on this machine |
| `/testery-run-playwright-bdd-on-testery` | Run playwright-bdd tests on Testery (local build OR remote Git) |

#### Playwright-BDD authoring

| Command | What it does |
|---|---|
| `/bdd-add-scenario` | Add a scenario, implement step defs, drive the red→green loop |
| `/bdd-test` | Run the playwright-bdd suite (or a single scenario by name) |
| `/bdd-implement-code` | Implement app code to make a failing scenario pass |
| `/bdd-view-report` | Open the Playwright HTML report in a browser |

### Skills

All `testery-*` skills wrap the [Testery CLI](https://github.com/testery/testery-cli) and load automatically when relevant. Read-only inspection (listing projects/runs/results) can also be served by the [Testery MCP server](https://github.com/testery/testery-mcp). The `testery-playwright-bdd-*` skills are modeled on `example-webapp/web/`.

## Prerequisites

1. **Claude Code** with plugin support.
2. **Testery CLI** on PATH (auto-installed by `/testery-onboard` if missing):
   ```bash
   pip install testery
   ```
3. **API token**: easiest via `/testery-onboard` (or `testery login`). Manual — the CLI falls back to `$TESTERY_API_TOKEN`:
   ```bash
   export TESTERY_API_TOKEN=<your-token>        # bash/zsh
   $env:TESTERY_API_TOKEN = '<your-token>'      # PowerShell
   ```
4. **Optional**: configure the Testery MCP server in Claude Code for richer read-only inspection.
5. **playwright-bdd skills** assume a project shaped like `example-webapp/web/` (`tests/features/`, `tests/steps/`, `playwright.config.ts` calling `defineBddConfig`, and a `test:e2e` script that runs `bddgen && playwright test`).

## Layout

```
testery-claude-plugin/
├── .claude-plugin/
│   ├── plugin.json          # plugin manifest
│   └── marketplace.json     # marketplace entry (this repo IS the marketplace)
├── commands/                # slash commands (auto-discovered)
│   ├── testery-*.md
│   └── bdd-*.md
└── skills/                  # skills (auto-discovered)
    ├── testery-*/SKILL.md
    └── testery-playwright-bdd-*/SKILL.md
```

Each slash command delegates to its corresponding skill, so the documented behavior lives in one place. For write operations (create test run, upload artifacts, schedules, environments, deploys, monitoring), skills shell out to the CLI.

## License

MIT
