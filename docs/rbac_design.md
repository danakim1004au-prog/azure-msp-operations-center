# RBAC Design

## Principles

- Use least privilege for MSP operators.
- Separate reader, responder, and administrator responsibilities.
- Prefer managed identity for automation.
- Avoid assigning Owner except for break-glass scenarios.
- Scope access at resource group when possible.

## Suggested Roles

| Persona | Azure Role | Scope | Reason |
| --- | --- | --- | --- |
| MSP L1 Support | Reader, Monitoring Reader | Customer RG | View resources and logs |
| MSP L2 Support | Monitoring Contributor, Log Analytics Reader | Customer RG / workspace | Create alert rules and investigate incidents |
| MSP Automation | Automation Contributor | Automation account | Run approved runbooks |
| Security Analyst | Microsoft Sentinel Reader / Responder | Sentinel workspace | Investigate security incidents |
| Platform Admin | Contributor | MSP operations RG | Manage platform resources |
| Break-glass Admin | Owner | Subscription | Emergency only |

## Automation Identity

The runbook managed identity should receive:

- Reader on monitored customer resource groups.
- Monitoring Reader on the Log Analytics workspace.
- Specific service roles only when remediation requires them.

Example remediation permissions:

| Remediation | Minimum Permission |
| --- | --- |
| Restart App Service | Website Contributor on target App Service |
| Start VM | Virtual Machine Contributor on target VM |
| Read Key Vault diagnostic state | Reader + Key Vault Reader |

## Portfolio Evidence To Capture

- Screenshot of role assignments.
- Explanation of why each role is needed.
- Example denied action proving least privilege.
- Break-glass policy and audit approach.
