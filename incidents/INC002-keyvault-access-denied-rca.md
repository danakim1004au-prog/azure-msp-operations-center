# INC002 - Key Vault Access Denied RCA

## Summary

Fabrikam Clinic appointment portal failed to retrieve database credentials from Key Vault after a managed identity access policy change.

## Impact

- Customer: `fabrikam-clinic`
- Environment: `prod`
- Service: App Service + Key Vault
- Severity: Sev2
- User impact: Appointment booking unavailable

## Timeline

| Time | Event |
| --- | --- |
| 14:02 | App Service dependency errors began |
| 14:04 | Key Vault access denied alert fired |
| 14:08 | AzureActivity showed access policy update |
| 14:16 | Correct Key Vault permission restored |
| 14:22 | Application health confirmed |

## Root Cause

The App Service managed identity lost permission to read the required Key Vault secret during a manual access policy update.

## Detection

`kql/identity/keyvault_access_denied.kql`

## Mitigation

Restored least-privilege secret read access for the App Service managed identity.

## Preventive Actions

- Manage Key Vault access through IaC.
- Add policy review for manual Key Vault changes.
- Add workbook panel for Key Vault authorization failures.
