# KQL Query Pack

This directory contains support-oriented KQL and Azure Resource Graph queries.

## Categories

| Directory | Purpose |
| --- | --- |
| `appservice/` | HTTP 5xx, latency, deployments |
| `sql/` | DTU saturation, deadlocks, failed connections |
| `vm/` | Heartbeat, CPU, disk, failed logons |
| `identity/` | Entra sign-ins, role changes, Key Vault failures |
| `cost/` | Cost anomaly and orphaned resource reviews |

## Usage

- Use Log Analytics queries in Azure Monitor alerts and Workbooks.
- Use Azure Resource Graph queries for governance and cost review.
- Save query output as incident evidence during RCA.
