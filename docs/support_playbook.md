# Support Playbook

## Severity Model

| Severity | Definition | Initial Response Target | Example |
| --- | --- | --- | --- |
| Sev1 | Customer production outage or severe data risk | 15 minutes | App unavailable for all users |
| Sev2 | Major degradation with workaround | 30 minutes | SQL saturation affecting checkout |
| Sev3 | Limited customer impact | 4 hours | Single VM heartbeat loss |
| Sev4 | Advisory or low-risk request | 1 business day | Cost review, tag cleanup |

## Triage Checklist

1. Confirm affected customer, environment, and workload.
2. Confirm start time, impact scope, and active symptoms.
3. Check recent changes in `AzureActivity`.
4. Run service-specific KQL investigation query.
5. Check dependency health: identity, Key Vault, SQL, network, storage.
6. Capture screenshots or query outputs for evidence.
7. Apply mitigation or rollback using approved runbook.
8. Send customer update.
9. Monitor recovery metrics.
10. Write RCA when impact is confirmed.

## Customer Update Templates

### Initial Response

Subject: Incident acknowledged - `<customer>` `<workload>`

We have acknowledged the incident affecting `<service>`. Initial symptoms show `<symptom>` starting around `<time>`. We are investigating recent changes, service health, and application telemetry. The next update will be provided by `<time>`.

### Mitigation Update

Subject: Mitigation in progress - `<customer>` `<workload>`

We identified `<probable cause>` and started mitigation using `<action>`. Current impact is `<impact>`. We are monitoring `<metric>` to confirm recovery.

### Final Update

Subject: Incident resolved - `<customer>` `<workload>`

The incident was resolved at `<time>`. Root cause was `<root cause>`. Preventive actions are `<actions>`. A full RCA is available in the incident record.

## Escalation Matrix

| Area | Escalate To | When |
| --- | --- | --- |
| Identity / RBAC | Security admin | Role assignment, SPN, conditional access failure |
| Network | Cloud network engineer | Private Endpoint, DNS, NSG, routing issue |
| Database | DBA / data platform engineer | SQL saturation, deadlock, failed backup |
| Application | App owner | Code deployment, dependency error |
| Customer approval | Service delivery manager | Any remediation with downtime or data impact |
