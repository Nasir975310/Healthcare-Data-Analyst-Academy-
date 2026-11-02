$ErrorActionPreference = 'Stop'
Write-Host '--- Repository ---'
git status --short
Write-Host "`n--- Staged file summary ---"
git diff --cached --stat
Write-Host "`n--- Staged whitespace / patch check ---"
git diff --cached --check
Write-Host "`n--- Sensitive file names (manual review required) ---"
git diff --cached --name-only | Select-String -Pattern '(^|/)(\.env|secrets?|credentials?)(/|$)|\.(pem|key)$|patient|mrn|medical_record'
Write-Host "`nThis is a preflight, not a DLP/security certification. Inspect staged content and repository visibility manually."
