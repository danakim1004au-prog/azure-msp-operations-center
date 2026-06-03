param(
    [Parameter(Mandatory = $true)]
    [string] $ResourceGroupName,

    [Parameter(Mandatory = $true)]
    [string] $VmName,

    [bool] $DryRun = $true
)

Write-Output "Runbook: start_vm"
Write-Output "Resource group: $ResourceGroupName"
Write-Output "VM: $VmName"
Write-Output "Dry run: $DryRun"

if ($DryRun) {
    Write-Output "Dry-run mode enabled. No VM start executed."
    return
}

Start-AzVM -ResourceGroupName $ResourceGroupName -Name $VmName
Write-Output "Start command submitted."
