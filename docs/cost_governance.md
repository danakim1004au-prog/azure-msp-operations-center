# Cost Governance

## Goals

- Detect unexpected cost increases early.
- Attribute costs by customer and environment.
- Identify idle or orphaned resources.
- Produce support-friendly monthly review notes.

## Cost Signals

| Signal | Detection |
| --- | --- |
| Daily spend spike | Daily cost exceeds 7-day average by threshold |
| Untagged resources | Azure Resource Graph query |
| Idle App Service plan | Empty or low-traffic plan |
| Unattached disks | Disk state is unattached |
| Unused public IP | No IP configuration |
| Oversized VM | Low CPU over rolling window |

## Monthly Review Format

| Section | Content |
| --- | --- |
| Executive summary | Customer-level cost trend |
| Top changes | New resources, SKU changes, scale events |
| Waste candidates | Orphaned resources and idle compute |
| Actions taken | Deleted, resized, reserved, or deferred |
| Risks | Items requiring customer approval |
