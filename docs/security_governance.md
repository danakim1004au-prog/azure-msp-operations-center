# Security Governance

## Required Controls

| Control | Implementation |
| --- | --- |
| Mandatory tags | Azure Policy |
| Diagnostic logs enabled | Azure Policy or deployment checklist |
| Public storage disabled | Azure Policy |
| Secrets separated from code | Key Vault |
| Automation authentication | Managed Identity |
| Operator access | RBAC groups |
| Change tracking | Azure Activity + incident notes |

## Security Detection Themes

- Excessive failed sign-ins.
- Sign-ins from unexpected countries.
- Privileged role assignment changes.
- Key Vault secret access failures.
- Public IP creation in production.
- Storage account public access changes.

## Governance Notes

This project should be demoed with synthetic customer names and non-production subscriptions. For real customer environments, Azure Lighthouse delegation and written customer approval are required before remediation automation is enabled.
