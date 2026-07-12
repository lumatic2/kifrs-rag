# kifrs-drift-weekly — KASB drift 주간 감지 task 등록 (재실행 가능, 기존 task 갱신)
# 실행: pwsh -File scripts/register_drift_task.ps1
$repo = Split-Path -Parent $PSScriptRoot
$py = Join-Path $repo ".venv\Scripts\python.exe"
$log = Join-Path $repo "data\drift\cron.log"

$action = New-ScheduledTaskAction -Execute "cmd.exe" `
    -Argument "/c cd /d `"$repo`" && `"$py`" -m kifrs.drift >> `"$log`" 2>&1"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 09:00
# StartWhenAvailable: 실행 시각에 PC 가 꺼져 있었으면 다음 기회에 실행
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

Register-ScheduledTask -TaskName "kifrs-drift-weekly" -Action $action `
    -Trigger $trigger -Settings $settings -Force
Write-Host "registered: kifrs-drift-weekly (weekly Mon 09:00, StartWhenAvailable)"
