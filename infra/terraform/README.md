# Terraform Infrastructure

This scaffold provisions the MSP operations center resources:

- Resource group
- Log Analytics Workspace
- Application Insights
- Storage account for incident/model artifacts
- Automation Account with system-assigned managed identity
- Azure Monitor Action Group
- Scheduled query alert examples
- Policy assignment example for customer tagging

## Deploy

```bash
terraform init
terraform plan -var="alert_email=you@example.com"
terraform apply -var="alert_email=you@example.com"
```

## Notes

- The policy assignment uses a built-in policy ID as a placeholder. Confirm the policy ID in your tenant before production use.
- The scheduled query alert rules reference KQL files under `../../kql`.
- Real customer onboarding should use Azure Lighthouse or explicit scoped RBAC assignment.
