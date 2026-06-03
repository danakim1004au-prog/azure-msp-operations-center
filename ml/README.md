# SLA Breach Prediction

This directory contains a lightweight ML workflow for the data team portion of the project.

## Feature Set

| Feature | Meaning |
| --- | --- |
| `recent_alerts_1h` | Number of recent alerts for the workload |
| `error_rate_15m` | Recent HTTP/application error rate |
| `cpu_p95_30m` | 30-minute CPU p95 |
| `failed_signins_30m` | Recent identity failures |
| `sql_dtu_max_30m` | SQL saturation indicator |
| `vm_heartbeat_gap_min` | VM monitoring gap |
| `deployment_within_2h` | Recent change risk |
| `keyvault_denials_30m` | Secret access failures |

## Run

```bash
python3 scripts/generate_synthetic_incidents.py
python3 ml/train_sla_model.py
python3 ml/score_incidents.py
```

## Interpretation

The prediction output is a prioritization signal for support triage. A high-risk incident should be reviewed earlier, but mitigation still requires human confirmation and customer-approved runbooks.
