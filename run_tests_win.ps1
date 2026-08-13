$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Pass = 0
$Fail = 0

function Run-Check($Label, $Command) {
    Invoke-Expression $Command | Out-Null
    if ($LASTEXITCODE -eq 0) { Write-Host "PASS $Label"; $script:Pass++ }
    else { Write-Host "FAIL $Label"; $script:Fail++ }
}

$Registry = Get-Content "$Root\src\framework\workflow-registry.json" | ConvertFrom-Json
foreach ($Item in $Registry.work_items) {
    $Validator = "$Root\$($Item.skill_path)\scripts\validate_artifact.py"
    $Fixtures = "$Root\test\skills\$($Item.id)\fixtures"
    foreach ($Fixture in Get-ChildItem "$Fixtures\*.md" -ErrorAction SilentlyContinue) {
        if ($Fixture.Name -like "*violation*") { continue }
        Run-Check "$($Item.id)/$($Fixture.Name)" "python3 `"$Validator`" `"$($Fixture.FullName)`" --json"
    }
}

foreach ($Test in Get-ChildItem "$Root\test" -Filter "test_*.py" -File -Recurse) {
    Run-Check "unit/$($Test.FullName.Substring($Root.Length + 6))" "python3 `"$($Test.FullName)`""
}

foreach ($Req in Get-ChildItem "$Root\requirements\REQ-*" -Directory) {
    Run-Check "status/$($Req.Name)" "python3 `"$Root\src\scripts\orchestrator.py`" `"$($Req.FullName)`" --json"
    Run-Check "records/$($Req.Name)" "python3 `"$Root\src\scripts\branch_validator.py`" `"$($Req.FullName)`" --json"
}

Write-Host "Result: $Pass passed / $Fail failed"
if ($Fail -gt 0) { exit 1 }
