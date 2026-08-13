$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Pass = 0
$Fail = 0

function Run-Check($Label, $Command) {
    Invoke-Expression $Command | Out-Null
    if ($LASTEXITCODE -eq 0) { Write-Host "PASS $Label"; $script:Pass++ }
    else { Write-Host "FAIL $Label"; $script:Fail++ }
}

function Run-NegativeCheck($Label, $Command) {
    # Inverted check: *violation* fixtures must be REJECTED by the validator.
    Invoke-Expression $Command | Out-Null
    if ($LASTEXITCODE -eq 0) { Write-Host "FAIL negative/$Label (validator did not reject violation)"; $script:Fail++ }
    else { Write-Host "PASS negative/$Label"; $script:Pass++ }
}

# ---- Phase 0: cross-document consistency (must pass before anything else) ----
Run-Check "consistency/registry-vs-docs" "python3 `"$Root\src\scripts\consistency_check.py`""

$Registry = Get-Content "$Root\src\framework\workflow-registry.json" | ConvertFrom-Json

# Main work items: fixture-test their validators
foreach ($Item in $Registry.work_items) {
    $Validator = "$Root\$($Item.skill_path)\scripts\validate_artifact.py"
    $Fixtures = "$Root\test\skills\$($Item.id)\fixtures"
    foreach ($Fixture in Get-ChildItem "$Fixtures\*.md" -ErrorAction SilentlyContinue) {
        if ($Fixture.Name -like "*violation*") {
            Run-NegativeCheck "$($Item.id)/$($Fixture.Name)" "python3 `"$Validator`" `"$($Fixture.FullName)`" --json"
            continue
        }
        Run-Check "$($Item.id)/$($Fixture.Name)" "python3 `"$Validator`" `"$($Fixture.FullName)`" --json"
    }
}

# Branch/support skills (registry-driven): syntax-check validators + fixture-test
foreach ($Cap in $Registry.support_capabilities) {
    $Validator = "$Root\$($Cap.skill_path)\scripts\validate_artifact.py"
    if (Test-Path $Validator) {
        Run-Check "branch-validator/$($Cap.id)" "python3 -c `"compile(open('$Validator').read(),'$Validator','exec')`""
    } else {
        Write-Host "FAIL missing branch validator $($Cap.id)"; $script:Fail++
    }
    $Fixtures = "$Root\test\skills\$($Cap.id)\fixtures"
    foreach ($Fixture in Get-ChildItem "$Fixtures\*.md" -ErrorAction SilentlyContinue) {
        if ($Fixture.Name -like "*violation*") {
            Run-NegativeCheck "branch-skill/$($Cap.id)/$($Fixture.Name)" "python3 `"$Validator`" `"$($Fixture.FullName)`" --json"
            continue
        }
        Run-Check "branch-skill/$($Cap.id)/$($Fixture.Name)" "python3 `"$Validator`" `"$($Fixture.FullName)`" --json"
    }
}

# Unit and integration tests
foreach ($Test in Get-ChildItem "$Root\test" -Filter "test_*.py" -File -Recurse) {
    Run-Check "unit/$($Test.FullName.Substring($Root.Length + 6))" "python3 `"$($Test.FullName)`""
}

# Requirement dirs (if any)
foreach ($Req in Get-ChildItem "$Root\requirements\REQ-*" -Directory) {
    Run-Check "status/$($Req.Name)" "python3 `"$Root\src\scripts\orchestrator.py`" `"$($Req.FullName)`" --json"
    Run-Check "records/$($Req.Name)" "python3 `"$Root\src\scripts\branch_validator.py`" `"$($Req.FullName)`" --json"
}

Write-Host "Result: $Pass passed / $Fail failed"
if ($Fail -gt 0) { exit 1 }
