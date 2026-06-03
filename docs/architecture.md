# Architecture

## Goal

Build an MSP-style Azure operations center for multi-customer monitoring, incident response, and SLA breach prediction.

The project emphasizes operational support skills:

- Centralized monitoring with Azure Monitor and Log Analytics.
- KQL-based investigation and alerting.
- Customer/environment tagging.
- Automated runbooks for repeatable response.
- SLA breach risk prediction from operational telemetry.
- RCA and support communication artifacts.

## Logical Components

| Component | Purpose |
| --- | --- |
| Log Analytics Workspace | Central place for platform, app, VM, and identity logs |
| Diagnostic Settings | Route supported resource logs to the workspace |
| Azure Monitor Alerts | Detect incident conditions from metrics and logs |
| Action Group | Notify and trigger automation |
| Automation Account | Run remediation scripts and evidence collection |
| Storage Account | Store exported logs, model output, runbook artifacts |
| Azure SQL Database | Optional incident table and scored SLA risks |
| Azure Workbook | Operations dashboard for MSP/customer review |
| Azure Policy | Enforce tags, diagnostics, and security controls |

## Customer Tagging Model

Every monitored resource should use these tags:

| Tag | Example | Purpose |
| --- | --- | --- |
| `customer` | `contoso-retail` | MSP customer ownership |
| `environment` | `prod` | Environment separation |
| `owner` | `cloud-ops` | Internal accountability |
| `criticality` | `high` | SLA and alert priority |
| `costCenter` | `cc-1001` | Cost analysis |

## Signal Sources

| Source | Example Tables | Use |
| --- | --- | --- |
| App Service | `AppServiceHTTPLogs`, `AppServiceAppLogs` | 5xx spike, latency, app errors |
| Azure SQL | `AzureDiagnostics`, metrics | DTU, deadlocks, failed connections |
| VMs | `Heartbeat`, `Perf`, `SecurityEvent` | availability, CPU, disk, failed logins |
| Entra ID | `SigninLogs`, `AuditLogs` | risky access, failed logins, role changes |
| Azure Activity | `AzureActivity` | resource changes, delete operations |
| Cost | Cost export or synthetic billing records | cost anomaly and idle resource review |

## Operational Flow

1. Customer resources emit logs to Log Analytics.
2. KQL queries detect symptoms and enrich incidents with tags.
3. Alert rules trigger action groups.
4. Runbooks collect evidence or execute safe remediation.
5. Incident records are stored for triage and model training.
6. Data pipeline builds rolling operational features.
7. SLA model predicts breach probability.
8. Workbook displays customer health, active incidents, and risk scores.
9. RCA documents capture root cause, mitigation, and prevention actions.

## High-Risk Design Areas

- Cross-customer data isolation must be clear.
- MSP operators should have least-privilege roles.
- Runbooks must support dry-run mode for customer-impacting actions.
- Alerts must avoid fatigue through severity mapping and suppression windows.
- Model predictions must not replace human triage; they prioritize review.
