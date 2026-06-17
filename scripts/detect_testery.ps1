# detect_testery - report the Testery CLI install + onboarding state.
#
#   exit 0 + "READY <version>"   CLI installed AND onboarded (token/credentials present)
#   exit 1 + "NOT_INSTALLED"     CLI not on PATH
#   exit 1 + "NOT_ONBOARDED"     CLI present but not authenticated yet
#
# Windows counterpart of detect_testery.sh. "Onboarded" = a token saved by
# `testery login` (~/.testery/credentials) or $env:TESTERY_API_TOKEN is set.
if (-not (Get-Command testery -ErrorAction SilentlyContinue)) {
    Write-Output "NOT_INSTALLED"
    exit 1
}
$creds = Join-Path $HOME ".testery/credentials"
if ($env:TESTERY_API_TOKEN -or (Test-Path $creds)) {
    $v = (& testery --version 2>$null | Select-Object -First 1)
    Write-Output "READY $v"
    exit 0
}
Write-Output "NOT_ONBOARDED"
exit 1
