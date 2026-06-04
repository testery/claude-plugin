<!-- markdownlint-disable MD033 MD041 -->
<div align="center">

# Testery for Claude Code

### AI writes the tests. Testery orchestrates them — fast and flake-free.

Your AI agent writes the code and the tests. Testery runs them fast and flake-free on every change, gates the deploy, and is the independent audit layer so your AI doesn't grade its own homework.

[![Marketplace](https://img.shields.io/badge/Claude_Code-marketplace-d97757)](https://testery.io/claude-plugin)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://github.com/testery/claude-plugin/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](#license)
[![Docs](https://img.shields.io/badge/docs-docs.testery.io-informational)](https://docs.testery.io)
[![Built for Claude Code](https://img.shields.io/badge/built_for-Claude_Code-8a3ffc)](https://code.claude.com)

[**Get started →**](https://testery.io/claude-plugin) &nbsp;•&nbsp; [Docs](https://docs.testery.io) &nbsp;•&nbsp; [testery.io](https://testery.io)

</div>

---

<!--
  Above-the-fold demo. Mirrors the live terminal story on the landing page:
  AI refactors checkout -> Claude runs the suite on Testery -> catches 2 real
  failures + 1 quarantined flake -> fixes them -> reruns only the failed tests
  -> proves the build green. Ends on "Verified on Testery, not assumed."

  docs/demo.gif is rendered from docs/claude-plugin-demo.cast (asciinema v2) with agg:
    agg --theme c9d4e3,0a0c10,0a0c10,ff5f6d,2ee06a,f4c152,5cc8ff,b88aff,4fd6c0,c9d4e3,5a6678,ff7b85,44f08a,ffd479,7fd6ff,c9a4ff,6fe6d2,ffffff \
        --text-font-family "Consolas,JetBrains Mono,DejaVu Sans Mono" \
        --emoji-font-family "Consolas,Segoe UI Symbol,DejaVu Sans Mono" \
        --speed 1.1 docs/claude-plugin-demo.cast docs/demo.gif
  The live animated demo is at https://testery.io/claude-plugin
-->
<div align="center">
  <a href="https://testery.io/claude-plugin">
    <img src="docs/demo.gif" alt="Claude Code using the Testery plugin: an AI refactors checkout, runs the suite on Testery, catches 2 real failures and a quarantined flake, fixes them, reruns only the failed tests, and proves the build green. Verified on Testery, not assumed." width="760">
  </a>
  <br>
  <em>Red turns green, <strong>verified on Testery, not assumed.</strong> &nbsp;(<a href="https://testery.io/claude-plugin">watch the live demo</a>)</em>
</div>

---

## The story

Your AI agent just refactored checkout. The diff looks clean. Ship it?

Not yet. The agent thinks the change works, but "the AI says it's fine" is not a passing test. So Claude runs the suite on Testery:

- Testery catches **2 real failures** the refactor introduced and **1 flaky test** it quarantines automatically, so the flake doesn't block the build or get mistaken for a real bug.
- Claude reads the failures, fixes the code, and reruns **only the tests that failed** instead of the whole suite.
- Testery proves the build green.

That is the Testery Loop, and it runs on every change. The agent writes the tests and the code. Testery is the independent referee that decides whether it actually works.

### Why this exists

If you have shipped software with AI in the loop, you know the pain:

- **Flaky tests** that fail at random and train everyone to ignore red.
- **"Works on my machine"** that doesn't survive contact with CI.
- **AI that confidently ships broken code**, because the same agent that wrote the change also declared it correct.

Testery is the test **orchestration and verification** platform for AI-driven development. It runs your suite fast and flake-free, quarantines and retries flakes so red means red, gates the deploy, and gives you an **independent audit** of what the AI produced.

**Don't let AI grade its own homework.**

---

**~28 slash commands. ~33 skills. One install.**

---

## Quickstart (green test in ~5 minutes)

Run these in Claude Code:

```text
# 1. Add the marketplace (the repo path) and install the plugin
/plugin marketplace add testery/claude-plugin
/plugin install testery@testery

# 2. Connect your account (signup or token, walked through for you)
/testery-onboard

# 3. Scaffold playwright-bdd tests and wire this repo to Testery
/testery-init

# 4. Author a scenario in plain language, let AI implement it, run it
/bdd-add-scenario
/bdd-implement-code
/bdd-test
```

You should see a scenario go **red, then green** on a local run. Local runs are **free and unmetered**, so the first win costs nothing. When you are ready for scale, run the same suite on Testery's cloud:

```text
/testery-create-test-run     # run on Testery infrastructure
/testery-monitor-test-run    # live dashboard, then a pass/fail summary
```

> **Note:** the install line is always `/plugin install testery@testery`. The marketplace name (`testery`) lives in `marketplace.json` and is independent of the repo name, so it never changes even if the repo is renamed. Only the `marketplace add` line points at the repo path.

---

## How it works: the Testery Loop

```text
  edit a plain-language          AI writes the              Testery runs the
  feature file        ───▶       code + tests     ───▶      suite (fast, flake-free)
                                                                    │
        ▲                                                           ▼
        │                                                  catches real failures,
   ship it, green                                          quarantines flakes
   and verified                                                     │
        │                                                           ▼
        └──────────────  AI + Testery iterate  ◀────────  rerun only what failed
```

1. **Describe the behavior.** Write or edit a Gherkin feature file in plain language.
2. **AI writes the code.** `/bdd-implement-code` implements the app code (not the test) to satisfy the scenario.
3. **Testery runs the tests.** Locally for free, or on the cloud for scale. Flakes are quarantined and retried so red means red.
4. **Iterate to green.** The AI reads real failures, fixes them, and reruns only what failed.
5. **Ship, verified.** The deploy is gated on a green run. Verified on Testery, not assumed.

---

## What you can do

Outcomes first. These are the jobs this plugin does, with the commands that matter most.

### Orchestrate and verify (the Testery platform)

| You want to... | Use |
| --- | --- |
| Run the suite fast and flake-free on every change | `/testery-create-test-run`, `/testery-monitor-test-run` |
| See which tests passed or failed | `/testery-report-test-run` |
| Quarantine and retry flakes, rerun only what failed | built into every run |
| Gate the deploy on a green run | `/testery-create-deploy`, `/testery-create-alert` |
| Schedule nightly or on-deploy runs | `/testery-create-schedule`, `/testery-list-schedules` |
| Manage environments (staging, qa, prod) | `/testery-register-environment`, `/testery-list-environments` |
| Connect your account once | `/testery-onboard`, `/testery-init`, `/testery-verify-token` |

### Author tests in plain language (Playwright-BDD)

| You want to... | Use |
| --- | --- |
| Add a scenario from a feature file | `/bdd-add-scenario` |
| Have AI implement the app code behind it | `/bdd-implement-code` |
| Run the red-to-green loop locally (free) | `/bdd-test` |
| View the Playwright HTML report | `/bdd-view-report` |

<details>
<summary><strong>Full command and skill reference (~28 commands, ~33 skills)</strong></summary>

### Testery platform commands

- `/testery-onboard`, `/testery-init`, `/testery-verify-token`
- `/testery-create-test-run`, `/testery-monitor-test-run`, `/testery-cancel-test-run`, `/testery-list-active-test-runs`, `/testery-list-test-runs`, `/testery-report-test-run`
- `/testery-upload-artifacts`, `/testery-add-file`
- `/testery-register-environment`, `/testery-update-environment`, `/testery-deregister-environment`, `/testery-list-environments`, `/testery-upload-environment-file`
- `/testery-create-schedule`, `/testery-list-schedules`, `/testery-delete-schedule`
- `/testery-create-deploy`, `/testery-create-alert`
- `/testery-run-test-plan`, `/testery-load-users`
- `/testery-run-playwright-bdd-local`, `/testery-run-playwright-bdd-on-testery`

### Playwright-BDD authoring commands

- `/bdd-add-scenario`, `/bdd-implement-code`, `/bdd-test`, `/bdd-view-report`

### Skills

Each command delegates to a matching skill, and the skills also load automatically when relevant. Plugin skills are namespaced under the plugin name, so they surface as `/testery:<skill-name>` in Claude Code, for example `/testery:testery-create-test-run`, `/testery:testery-monitor-test-run`, or `/testery:testery-playwright-bdd-add-scenario`. Additional authoring-only skills include `testery-playwright-bdd-add-step-definition` and `testery-playwright-bdd-add-page-object`. Run `/help` after install to see the complete list with the exact strings to type.

</details>

---

## Plugin vs MCP: one client of many

Testery exposes a **portable MCP server** ([github.com/testery/testery-mcp](https://github.com/testery/testery-mcp)) as the connection layer to the platform. It speaks the open Model Context Protocol, so it works in Cursor, Copilot, Windsurf, VS Code, and any MCP-compatible client. **This Claude Code plugin is one client of many,** so you are not locked to a single tool.

The plugin is the **batteries-included Claude Code experience**: it wires up that MCP server plus every command and skill above, preconfigured, the moment you install it. Prefer scripts and CI? The [Testery CLI](https://github.com/testery/testery-cli) drives the same platform from the command line.

| Repo | Role |
| --- | --- |
| [testery-mcp](https://github.com/testery/testery-mcp) | The portable connection layer (any MCP client) |
| this repo | The batteries-included Claude Code plugin |
| [testery-cli](https://github.com/testery/testery-cli) | The command-line runner for CI and scripts |

---

## What this installs

When you install `testery@testery`, you get the commands and skills listed above. Claude Code shows a per-plugin context-cost estimate at install time, so you can see the footprint before you confirm.

- **Local runs are free and unmetered.** Author, run the red-to-green loop, and verify locally at no cost.
- **You pay only for cloud scale.** Cloud runs on Testery infrastructure (parallelism, hosted browsers, history, reporting) are the paid tier.

---

## Prerequisites

- [Claude Code](https://code.claude.com) (current version).
- Node.js 18+ for Playwright-BDD authoring and local runs.
- A Testery account for cloud runs. `/testery-onboard` walks you through signup or a token. Local runs are free and do not require an account.

The `bdd-*` authoring helpers assume a playwright-bdd project (a `tests/features/` + `tests/steps/` layout, a `playwright.config.ts` that calls `defineBddConfig`, and a `test:e2e` script that runs `bddgen && playwright test`). `/testery-init` scaffolds exactly this for you.

---

## Update and uninstall

```text
# Update to the latest plugin version
/plugin marketplace update testery
/plugin install testery@testery

# Remove it
/plugin uninstall testery@testery
```

---

## Repository structure

This repo **is** the marketplace. The marketplace name is `testery`, the single plugin is `testery`, and its source is the repo root.

```text
claude-plugin/
├── .claude-plugin/
│   ├── marketplace.json     # marketplace "testery" -> plugin "testery" (source "./")
│   └── plugin.json          # name, version, repository, license, keywords
├── commands/                # ~28 slash commands
├── skills/                  # ~33 skills
├── docs/                    # demo asset (claude-plugin-demo.cast -> demo.gif)
└── README.md
```

Keywords: `testery`, `testing`, `playwright`, `playwright-bdd`, `cucumber`, `ci`, `test-orchestration`.

> **Roadmap note:** v0.1.0 ships as a single plugin so install is one step and everything is on. If the bundled footprint grows, the natural seam is to split a `testery-playwright-bdd` authoring plugin out of the core `testery` platform plugin inside the same `marketplace.json`. That preserves `@testery` and lets non-BDD users install only the core. No change for now.

---

## Contributing

Issues and PRs are welcome. If you are adding a command or skill, keep the namespaced invocation (`/testery:<skill-name>`) and the documented top-level commands (`/testery-onboard`, `/bdd-add-scenario`, ...) consistent so the README and `/help` agree.

## License

MIT. See [LICENSE](LICENSE).

---

<div align="center">

### Ready to stop assuming and start verifying?

[**Get started in Claude Code →**](https://testery.io/claude-plugin)

[Live demo](https://testery.io/claude-plugin) &nbsp;•&nbsp; [Docs](https://docs.testery.io) &nbsp;•&nbsp; [testery.io](https://testery.io)

*AI writes the tests. Testery orchestrates them — fast and flake-free.*

</div>
