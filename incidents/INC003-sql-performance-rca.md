# INC003 - Azure SQL Saturation RCA

## Summary

Contoso Retail production Azure SQL Database reached sustained DTU saturation, causing slow API responses.

## Impact

- Customer: `contoso-retail`
- Environment: `prod`
- Service: Azure SQL
- Severity: Sev2
- User impact: Slow checkout and product search

## Timeline

| Time | Event |
| --- | --- |
| 18:40 | SQL DTU alert fired |
| 18:44 | L2 reviewed DTU and query telemetry |
| 18:51 | App team confirmed promotional traffic spike |
| 19:03 | Temporary scale-up approved |
| 19:18 | Response time returned to acceptable range |

## Root Cause

Traffic exceeded the provisioned SQL capacity during a promotion. Query workload had insufficient headroom.

## Detection

`kql/sql/sql_dtu_saturation.kql`

## Mitigation

Temporarily scaled SQL tier and monitored API latency, DTU, and failed connection counts.

## Preventive Actions

- Add traffic forecast review before promotions.
- Add query tuning task for top expensive statements.
- Add autoscale or scheduled scale-up procedure where applicable.
