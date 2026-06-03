# Demo Script

## 1. Open With the Problem

This project simulates an MSP operations center for multiple Azure customers. The goal is not only to deploy cloud resources, but to detect incidents, investigate with KQL, predict SLA risk, and produce support-ready RCA documentation.

## 2. Show Architecture

Point to `docs/architecture.md`.

Explain:

- Customer resources send logs to Log Analytics.
- KQL rules detect operational symptoms.
- Action groups and runbooks support repeatable response.
- Data team transforms incident telemetry into SLA breach risk features.
- Workbooks give the MSP and customer a shared operational view.

## 3. Show Terraform

Open `infra/terraform/main.tf`.

Highlight:

- Log Analytics Workspace
- Application Insights
- Storage for artifacts
- Automation Account with managed identity
- Action Group
- Scheduled query alert examples
- Policy assignment for required customer tag

## 4. Show KQL

Open these examples:

- `kql/appservice/appservice_5xx_spike.kql`
- `kql/vm/vm_heartbeat_missing.kql`
- `kql/identity/keyvault_access_denied.kql`
- `kql/cost/orphaned_managed_disks_arg.kql`

Explain how each query maps to a real support ticket.

## 5. Run ML Workflow

```bash
python3 scripts/generate_synthetic_incidents.py
python3 ml/train_sla_model.py
python3 ml/score_incidents.py
```

Show:

- `data/raw/synthetic_incidents.csv`
- `ml/evaluation.md`
- `data/processed/scored_incidents.csv`

## 6. Show RCA

Open:

- `incidents/INC001-appservice-5xx-rca.md`
- `incidents/INC002-keyvault-access-denied-rca.md`
- `incidents/INC003-sql-performance-rca.md`

Explain that this is where the project becomes support-oriented rather than just deployment-oriented.

## 7. Close With Role Fit

This project demonstrates Azure support readiness: monitoring, KQL, RBAC, governance, automation, customer communication, and data-driven prioritization.
