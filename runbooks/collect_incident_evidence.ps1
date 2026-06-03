param(
    [Parameter(Mandatory = $true)]
    [string] $IncidentId,

    [Parameter(Mandatory = $true)]
    [string] $Customer,

    [Parameter(Mandatory = $true)]
    [string] $ResourceId
)

Write-Output "Collecting evidence for $IncidentId"
Write-Output "Customer: $Customer"
Write-Output "Resource: $ResourceId"
Write-Output "Recommended evidence:"
Write-Output "- AzureActivity changes around incident start time"
Write-Output "- Service-specific KQL query output"
Write-Output "- Resource Health and Service Health status"
Write-Output "- Current RBAC assignments if identity-related"
Write-Output "- Recent deployment or configuration changes"
