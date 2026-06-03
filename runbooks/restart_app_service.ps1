param(
    [Parameter(Mandatory = $true)]
    [string] $ResourceGroupName,

    [Parameter(Mandatory = $true)]
    [string] $AppServiceName,

    [bool] $DryRun = $true
)

Write-Output "Runbook: restart_app_service"
Write-Output "Resource group: $ResourceGroupName"
Write-Output "App Service: $AppServiceName"
Write-Output "Dry run: $DryRun"

if ($DryRun) {
    Write-Output "Dry-run mode enabled. No restart executed."
    return
}

Restart-AzWebApp -ResourceGroupName $ResourceGroupName -Name $AppServiceName
Write-Output "Restart command submitted."
