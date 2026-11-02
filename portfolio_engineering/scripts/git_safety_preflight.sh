#!/usr/bin/env bash
set -euo pipefail
echo '--- Repository ---'
git status --short
echo
echo '--- Staged file summary ---'
git diff --cached --stat
echo
echo '--- Staged whitespace / patch check ---'
git diff --cached --check
echo
echo '--- Sensitive file names (manual review required) ---'
git diff --cached --name-only | grep -Ei '(^|/)(\.env|secrets?|credentials?)(/|$)|\.(pem|key)$|patient|mrn|medical_record' || true
echo
echo 'This is a preflight, not a DLP/security certification. Inspect staged content and repository visibility manually.'
