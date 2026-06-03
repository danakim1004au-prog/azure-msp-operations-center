# Alert Matrix

| Alert | Source | Severity | Query | Primary Action |
| --- | --- | --- | --- | --- |
| App Service 5xx spike | AppServiceHTTPLogs | Sev2 | `kql/appservice/appservice_5xx_spike.kql` | Check deployment and dependency errors |
| App Service latency degradation | AppServiceHTTPLogs | Sev3 | `kql/appservice/appservice_latency_degradation.kql` | Review p95 latency and scale state |
| SQL DTU saturation | AzureDiagnostics | Sev2 | `kql/sql/sql_dtu_saturation.kql` | Review query load and scale option |
| SQL deadlocks | AzureDiagnostics | Sev2 | `kql/sql/sql_deadlocks.kql` | Escalate to DBA/app owner |
| SQL failed connections | AzureDiagnostics | Sev2 | `kql/sql/sql_failed_connections.kql` | Check identity, firewall, connection strings |
| VM heartbeat missing | Heartbeat | Sev2 | `kql/vm/vm_heartbeat_missing.kql` | Check VM power/network/agent |
| VM CPU pressure | Perf | Sev3 | `kql/vm/vm_cpu_pressure.kql` | Review process load and resize |
| VM low disk space | Perf | Sev2 | `kql/vm/vm_disk_free_space.kql` | Clean disk or expand volume |
| Failed VM logons | SecurityEvent | Sev2 | `kql/vm/vm_failed_logons.kql` | Security review |
| Failed Entra sign-ins | SigninLogs | Sev2 | `kql/identity/entra_failed_signins.kql` | Identity triage |
| Privileged role change | AuditLogs | Sev2 | `kql/identity/entra_privileged_role_changes.kql` | Verify change ticket |
| Key Vault access denied | AzureDiagnostics | Sev2 | `kql/identity/keyvault_access_denied.kql` | Check managed identity and access policy |
| Cost anomaly | Cost export | Sev4 | `kql/cost/daily_cost_anomaly.kql` | Cost review |
| Untagged resources | Azure Resource Graph | Sev4 | `kql/cost/untagged_resources_arg.kql` | Governance cleanup |

## Alert Tuning Notes

- Start with conservative thresholds to avoid alert fatigue.
- Use customer criticality tags to adjust severity.
- Suppress duplicate alerts during active incidents.
- Attach KQL output to incident notes for RCA evidence.
