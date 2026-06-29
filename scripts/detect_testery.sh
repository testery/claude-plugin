#!/usr/bin/env bash
# detect_testery - report the Testery CLI install + onboarding state.
#
#   exit 0 + "READY <version>"   CLI installed AND onboarded (token/credentials present)
#   exit 1 + "NOT_INSTALLED"     CLI not on PATH
#   exit 1 + "NOT_ONBOARDED"     CLI present but not authenticated yet
#
# The testery-* skills run this once per session before their first `testery`
# call. It is a cheap local check (no network) and a no-op when already READY,
# so it does not slow down commands. "Onboarded" = a token has been saved by
# `testery login` (~/.testery/credentials) or $TESTERY_API_TOKEN is set.
if ! command -v testery >/dev/null 2>&1; then
  echo "NOT_INSTALLED"
  exit 1
fi
if [ -n "${TESTERY_API_TOKEN:-}" ] || [ -s "$HOME/.testery/credentials" ]; then
  echo "READY $(testery --version 2>/dev/null | head -1)"
  exit 0
fi
echo "NOT_ONBOARDED"
exit 1
