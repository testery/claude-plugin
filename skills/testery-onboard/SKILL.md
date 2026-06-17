---
name: testery-onboard
description: Frictionless Testery onboarding — create a free account or connect an existing one, authenticate the CLI, and persist credentials. Asks the key questions up front (one batch) and only follows up if needed. Use at the start of any Testery work, when the preflight reports NOT_ONBOARDED, or when the user says "set up Testery", "I don't have an account yet", "log me in", or "where do I get a token?"
---

# Testery onboarding

Goal: end with the `testery` CLI authenticated and persisted (a token in `~/.testery/credentials`),
having **created a free account or connected an existing one** with the fewest possible questions.
Record the user's onboarding answers in `~/.testery/onboarding.json` so we never re-ask the same
things.

This skill is the convergence point for setup: run it when invoked directly, or when the preflight
(`detect_testery` / the PreToolUse guard) reports the CLI is present but `NOT_ONBOARDED`.

Authentication always goes through the CLI's **`testery login`** command, so the mechanism can
improve over time (token paste today, browser OAuth later) without changing this skill.

## 0. Don't re-ask — check prior state first

If `~/.testery/onboarding.json` exists:
- `completed_at` set **and** `testery verify-token` prints `Valid token` → already onboarded;
  confirm and stop.
- `declined_at` set this session → the user already chose "not now"; do **not** re-prompt. Briefly
  note they can run `/testery-onboard` anytime, and stop.

## 1. Ensure the CLI is installed

Use the canonical detect-and-install flow from the `testery-cli-setup` skill (run `detect_testery`;
if `NOT_INSTALLED`, show the welcome and offer to install). Continue once the CLI is present.

## 2. Already authenticated?

```bash
testery verify-token
```
`Valid token` → record `completed_at` (step 5) and stop. Otherwise continue.

## 3. Ask the onboarding questions — all at once

Make a **single `AskUserQuestion` call with both questions** (don't drip-feed). Only ask follow-ups
later if the chosen path needs them.

- **Question "Account"** — "Do you have a Testery account?"
  - `Create a free account` (recommended) — opens signup in the browser
  - `Connect an existing account`
  - `I have an API token` — paste a token directly
- **Question "Sign-in"** — "How should the CLI authenticate?"
  - `Open my browser` (recommended)
  - `Headless / paste a token` — for CI, SSH, or no browser available

Immediately persist these answers (step 5, with `completed_at` still null).

## 4. Complete the chosen path

- **Create a free account:** open `https://testery.app/signup`, then continue with login below.
  - Windows: `Start-Process "https://testery.app/signup"` (PowerShell) / `cmd //c start "https://testery.app/signup"` (git bash)
  - macOS: `open "https://testery.app/signup"` · Linux: `xdg-open "https://testery.app/signup"`
- **Log in (existing account, or right after signup):**
  ```bash
  testery login            # opens the browser; add --profile <name> for a named profile
  ```
  `testery login` opens the browser; the user approves/copies, and the CLI saves the token to
  `~/.testery/credentials`. If they chose **Headless / browser didn't open**, `testery login`
  prints the URL to open manually and accepts a pasted code/token.
- **Older CLI without `login`** (check `testery login --help`): open `https://testery.app` →
  Account Settings → API Keys, have the user copy a token, then store it:
  ```bash
  export TESTERY_API_TOKEN="<token>"      # bash/zsh   (PowerShell: $env:TESTERY_API_TOKEN = "<token>")
  ```
  or save it to the default profile in `~/.testery/credentials`.
- **I have an API token:** ask for the token (a follow-up), then save it the same way.

Never echo the token in tool output.

## 5. Persist onboarding answers to `~/.testery/onboarding.json`

Store the (non-secret) answers so future sessions don't re-ask. **Never put a token here** — tokens
live only in `~/.testery/credentials`.

POSIX:
```bash
mkdir -p ~/.testery
cat > ~/.testery/onboarding.json <<JSON
{
  "version": 1,
  "account_status": "<new|existing|token>",
  "auth_method": "<browser|token|env>",
  "profile": "default",
  "declined_at": null,
  "completed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON
chmod 600 ~/.testery/onboarding.json
```
PowerShell:
```powershell
New-Item -ItemType Directory -Force "$HOME/.testery" | Out-Null
@{ version = 1; account_status = "<...>"; auth_method = "<...>"; profile = "default"; declined_at = $null; completed_at = (Get-Date).ToUniversalTime().ToString("o") } | ConvertTo-Json | Set-Content "$HOME/.testery/onboarding.json"
```
- If the user picks **"Not now"**: write the file with `declined_at` set (timestamp) and
  `completed_at` null, then stop — the preflight will respect it and not re-nag this session.
- After a **successful** `testery verify-token`: write it with `completed_at` set.

## 6. Verify

```bash
testery verify-token
```
Confirm `Valid token` to the user.

## 7. What's next

Suggest `/testery-init` (no test project yet) or `/testery-list-environments`.

## Security notes

- Tokens are secret: never echo, log, or place them in `onboarding.json`. They belong only in
  `~/.testery/credentials` (managed by `testery login`; per-user, chmod 600).
- Rotate by re-running `testery login`, or delete `~/.testery/credentials` and log in again.
- CI: skip interactive login; set `TESTERY_API_TOKEN` as a secret instead.

## When this skill is NOT needed

- `onboarding.json` has `completed_at` and `testery verify-token` prints `Valid token`.
