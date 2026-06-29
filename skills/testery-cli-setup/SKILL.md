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

1. **Ensure the CLI is installed (canonical detect-and-offer flow).** Run this **once per
   session**, before the first `testery` call. It is a no-op when the CLI is already present,
   so it does **not** slow down commands. Do **not** `pip install` or run `testery --help`
   before *every* command.

   **a. Detect.** Run the bundled detection script (a cheap builtin check, no network):

   - POSIX shell (macOS, Linux, Git Bash on Windows):
     ```bash
     bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"
     ```
   - Windows PowerShell:
     ```powershell
     & "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"
     ```

   It prints one of `READY <version>` (exit 0), `NOT_INSTALLED` (exit 1), or
   `NOT_ONBOARDED` (exit 1).

   **b. If `READY`** — the CLI is installed and authenticated; continue, nothing more to do.

   **c. If `NOT_INSTALLED`** (and you have not already offered this session):
   1. Display this message to the user, exactly:

      > Your AI-enabled testing journey with Testery is about to begin! 🤖

   2. Use the **AskUserQuestion** tool to ask a yes/no question about installing the Testery
      CLI — frame the upside, e.g. header `Install CLI`, question "Install the Testery CLI? It
      unlocks running tests on Testery's cloud, live monitoring, schedules, environments, and
      more.", options **Yes, install it** / **Not now**.
   3. **If yes**, install it, then re-run the detect script (it will now report
      `NOT_ONBOARDED` — continue with **d**):
      - POSIX: `python3 -m pip install -q testery || python -m pip install -q testery`  (or `pipx install testery`)
      - PowerShell: `python -m pip install -q testery`  (or `py -m pip install -q testery`)
   4. **If no**, tell the user that Testery commands will not work until the CLI is installed,
      and do **not** re-ask for the rest of this session.

   **d. If `NOT_ONBOARDED`** (CLI installed but not authenticated): run the **testery-onboard**
   skill to sign the user in (signup or API-token paste; it saves credentials to
   `~/.testery/credentials`). After it completes, re-run the detect script — it should now
   print `READY`.

   Python may be `python3`, `python`, or the `py -3` launcher depending on the OS.

2. Verify auth (uses stored credentials / `$TESTERY_API_TOKEN` if no `--token` given):
   ```bash
   TESTERY_SKILL="testery-cli-setup" testery verify-token
   ```
   It prints `Valid token` on success.

3. If verification fails, run `testery login` (or the `testery-onboard` skill) to authenticate.

## Notes

- The CLI source of truth is `testery.py` in the `testery-cli` repo: pass `--help` to any subcommand for full options.
- For read-only inspection (list projects/runs/results), the Testery MCP server can be used instead when configured.
