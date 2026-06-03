# Runbooks

These PowerShell runbooks demonstrate MSP-safe automation patterns.

## Safety Model

- All customer-impacting runbooks default to `DryRun = true`.
- Real remediation should require incident ID, customer approval, and scoped RBAC.
- Runbook output should be attached to the incident record.

## Included Runbooks

| Runbook | Purpose |
| --- | --- |
| `restart_app_service.ps1` | Restart an App Service after approval |
| `start_vm.ps1` | Start a VM that is stopped unexpectedly |
| `collect_incident_evidence.ps1` | Print the evidence checklist for RCA |
