# Project Report: Azure MSP Operations Center
## Multi-Tenant Monitoring, Incident Response & SLA Prediction

---

## Scope of Work

| Area | Deliverable |
|---|---|
| Infrastructure as Code | Terraform deployment of all core resources |
| Monitoring Architecture | Log Analytics Workspace as central telemetry hub |
| Automation | Automation Account + Managed Identity + Runbook structure |
| Alerting | Azure Monitor Action Group |
| KQL Query Pack | App Service, VM, SQL, Identity, Cost |
| Workbook | Azure Workbook scaffold |
| Incident Data | 750-record synthetic incident dataset |
| ML Model | SLA breach prediction — training + scoring |
| RCA Documentation | 3 Root Cause Analysis reports |
| Operational Docs | Support Playbook, RBAC Design, Security Governance, Cost Governance |

---

## Resources Deployed

| Resource | Name |
|---|---|
| Resource Group | `rg-mspops-dev-u1r9mk` |
| Log Analytics Workspace | `law-mspops-dev-u1r9mk` |
| Application Insights | `appi-mspops-dev-u1r9mk` |
| Automation Account | `aa-mspops-dev-u1r9mk` |
| Action Group | `ag-mspops-dev-u1r9mk` |
| Storage Account | *(provisioned)* |
| Storage Containers | `incident-artifacts`, `model-outputs` |
| Policy Assignment | Required `customer` tag enforced at Resource Group level |

All resources were destroyed after deployment verification. The project is preserved through code, documentation, and output artefacts in this repository.

---

## Validation

| Check | Result |
|---|---|
| Terraform apply | Successful |
| Terraform output | Values confirmed correct |
| Terraform plan (post-apply) | No changes. Infrastructure matches configuration. |
| Python syntax check | Passed |
| Synthetic incident dataset (750 records) | Generated |
| SLA prediction model | Trained and scored |
| GitHub push | Verified |

---

## Technical Challenges & Resolutions

### 1. Alert Rule Deployment Against Empty Log Analytics Workspace

**Problem:** Two scheduled query alert rules referenced `AppServiceHTTPLogs` and `Heartbeat` tables. With no App Service or VM diagnostic logs yet connected, deploying these rules against an empty workspace would fail.

**Resolution:** Added an `enable_alert_rules` flag defaulting to `false`, with `count` conditionals on the alert resources. Core resources deploy first; alerts are activated separately once the required diagnostic tables exist.

```hcl
variable "enable_alert_rules" {
  description = "Create scheduled query alert rules after required Log Analytics tables exist."
  type        = bool
  default     = false
}
```

```hcl
count = var.enable_alert_rules ? 1 : 0
```

---

### 2. Azure Policy 403 — Missing Required Tag

**Problem:** A Resource Group–scoped policy required a `customer` tag on all resources. The default `required_tags` map in `variables.tf` omitted this tag, causing `RequestDisallowedByPolicy` on every resource creation.

**Resolution:** Added `customer` to the default tag set.

```hcl
default = {
  owner       = "cloud-ops"
  environment = "dev"
  costCenter  = "msp-demo"
  customer    = "msp-operations"
}
```

---

### 3. Terraform State Drift After Partial Apply

**Problem:** A partial `apply` provisioned the Log Analytics Workspace in Azure but left it untracked in Terraform state. Subsequent runs failed with a resource conflict requiring an import.

**Resolution:** Imported the existing resource into state, then re-ran `plan` and `apply`.

```bash
terraform import azurerm_log_analytics_workspace.ops "<workspace-resource-id>"
```

State and live resources were realigned. This highlighted the importance of idempotent deployments and explicit state management — particularly relevant in MSP environments where multiple engineers may touch the same infrastructure.
