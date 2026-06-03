---
name: testery-onboard
description: One-shot Testery auth onboarding: verifies an existing token, or walks a new user through signup/login at testery.io and persists their API key. Use at the start of any Testery work, or when the user says "set up Testery", "I don't have a Testery account yet", "log me in", or "where do I get a token?"
---

# Testery onboarding (signup / login / token persistence)

Goal: end this skill with the `testery` CLI authenticated and persisted across sessions (via `~/.testery/credentials`), regardless of whether the user had a Testery account when they started.

The CLI ships a first-class `testery login` command — prefer it over hand-writing credential files.

## Decision tree

1. **CLI present?** Run `testery --help`. If missing:
   ```bash
   pip install testery
   ```
   (or `pipx install testery` if pip isn't available system-wide).

2. **Already authenticated?** Run:
   ```bash
   testery verify-token
   ```
   It checks (in order) any `--token`, `--profile`, `~/.testery/credentials`, then `$TESTERY_API_TOKEN`. Prints `Valid token` on success.
   - Success → done. Confirm to the user and stop.
   - Failure → fall through to step 3.

3. **New user without an account?** Have them sign up first (free), then come back and log in:
   - Open `https://testery.app/signup`:
     - Windows: `Start-Process "https://testery.app/signup"` (PowerShell) or `cmd //c start "https://testery.app/signup"` (git bash)
     - macOS: `open "https://testery.app/signup"`
     - Linux: `xdg-open "https://testery.app/signup"`

4. **Log in via the CLI.** Run:
   ```bash
   testery login            # add --profile <name> to store under a named profile
   ```
   This opens the API-keys page in a browser. The user creates/copies a token and pastes it (or the redirect URL containing it) back into the CLI, which saves it to `~/.testery/credentials`. Treat the token as secret: never echo it in tool output.

   If a browser can't be opened (headless/CI), instead direct the user to **Account Settings → API Keys** at `https://testery.app`, then set the token as an environment variable:
   ```bash
   export TESTERY_API_TOKEN="<token>"      # bash/zsh
   $env:TESTERY_API_TOKEN = "<token>"      # PowerShell
   ```

5. **Re-verify.** Run `testery verify-token`. Confirm success (`Valid token`) to the user.

6. **Tell them what's next.** Suggest `/testery-init` (if they don't have a test project yet) or `/testery-list-environments` to see what's already configured.

## Security notes

- Never paste the token into chat output, log files, or commit it. `~/.testery/credentials` is per-user; `testery login` manages it for you.
- To rotate the token, re-run `testery login` (overwrites the profile), or delete `~/.testery/credentials` and log in again.
- For CI: skip the interactive login. Set `TESTERY_API_TOKEN` as a secret in the CI environment instead (every command falls back to it).

## When this skill is NOT needed

- `testery verify-token` already prints `Valid token` (a valid `~/.testery/credentials` or `$TESTERY_API_TOKEN` is present).
