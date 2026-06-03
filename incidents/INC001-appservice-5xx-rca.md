# INC001 - App Service 5xx Spike RCA

## Summary

Contoso Retail production checkout API returned elevated HTTP 500 responses for 23 minutes.

## Impact

- Customer: `contoso-retail`
- Environment: `prod`
- Service: App Service checkout API
- Severity: Sev2
- User impact: Checkout failures for a subset of requests

## Timeline

| Time | Event |
| --- | --- |
| 09:12 | Azure Monitor alert fired for App Service 5xx spike |
| 09:15 | L1 acknowledged and ran App Service 5xx query |
| 09:21 | Recent deployment found in AzureActivity |
| 09:29 | App owner rolled back deployment |
| 09:35 | Error rate returned to baseline |

## Root Cause

A deployment introduced an invalid downstream API configuration. The App Service returned 500 errors when checkout requests invoked that dependency.

## Detection

`kql/appservice/appservice_5xx_spike.kql`

## Mitigation

The application team rolled back the deployment. MSP operations monitored error rate and request volume until recovery.

## Preventive Actions

- Add deployment slot smoke test before production swap.
- Add alert for post-deployment 5xx increase.
- Require app owner approval for high-criticality production deployment.
