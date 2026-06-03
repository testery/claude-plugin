---
name: testery-cli-setup
description: Verify the Testery CLI is installed and authenticated. Use before invoking any other testery-* skill if auth has not been confirmed in the current session.
---

# Testery CLI setup

Every other `testery-*` skill in this collection shells out to the `testery` CLI. This skill confirms the CLI is on PATH and the API token is valid.

## Authentication

Every `testery` command accepts `--token` and `--profile`, and falls back to stored credentials when neither is passed. Auth resolution (as documented by `testery <command> --help`):

1. Explicit `--token <value>` flag
2. `--profile <name>` → that profile in `~/.testery/credentials`
3. `~/.testery/credentials` (written by `testery login`; `default` profile)
4. `$TESTERY_API_TOKEN` env var

The simplest setup is `testery login`, which opens the API-keys page in a browser and saves the token to `~/.testery/credentials` (optionally under `--profile <name>`). After that, commands authenticate with no `--token` needed.

If the user has never set up Testery on this machine, prefer the `testery-onboard` skill, which wraps `testery login`.

> Note: many example commands in this collection show `--token "$TESTERY_TOKEN"`. That still works if you export `TESTERY_TOKEN` yourself, but it is optional — once `testery login` has run (or `$TESTERY_API_TOKEN` is set), you can omit `--token` entirely.

## Steps

1. Check the CLI is installed:
   ```bash
   testery --help
   ```
   If missing, install: `pip install testery` (or `pip install -e <path-to-testery-cli>`).

2. Verify auth (uses stored credentials / `$TESTERY_API_TOKEN` if no `--token` given):
   ```bash
   testery verify-token
   ```
   It prints `Valid token` on success.

3. If verification fails, run `testery login` (or the `testery-onboard` skill) to authenticate.

## Notes

- The CLI source of truth is `testery.py` in the `testery-cli` repo: pass `--help` to any subcommand for full options.
- For read-only inspection (list projects/runs/results), the Testery MCP server can be used instead when configured.
