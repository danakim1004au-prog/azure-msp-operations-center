"""Generate synthetic MSP support incidents for SLA breach modeling."""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "synthetic_incidents.csv"

CUSTOMERS = ["contoso-retail", "fabrikam-clinic", "northwind-campus"]
SERVICES = ["appservice", "sql", "vm", "identity", "storage"]
SEVERITIES = ["Sev1", "Sev2", "Sev3", "Sev4"]


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + pow(2.718281828, -value))


def generate_row(index: int) -> dict[str, object]:
    customer = random.choice(CUSTOMERS)
    service = random.choices(SERVICES, weights=[32, 24, 22, 14, 8])[0]
    severity = random.choices(SEVERITIES, weights=[8, 32, 42, 18])[0]
    criticality = "high" if customer in {"contoso-retail", "fabrikam-clinic"} else "medium"

    recent_alerts_1h = random.randint(0, 24)
    error_rate_15m = round(random.betavariate(1.2, 10.0) * 0.5, 4)
    cpu_p95_30m = round(random.triangular(15, 99, 55), 2)
    failed_signins_30m = random.randint(0, 80 if service == "identity" else 18)
    sql_dtu_max_30m = round(random.triangular(5, 100, 45), 2) if service == "sql" else 0.0
    vm_heartbeat_gap_min = random.randint(0, 50) if service == "vm" else 0
    deployment_within_2h = 1 if service == "appservice" and random.random() < 0.35 else 0
    keyvault_denials_30m = random.randint(0, 15) if service in {"identity", "appservice"} else 0

    severity_weight = {"Sev1": 2.0, "Sev2": 1.2, "Sev3": 0.4, "Sev4": -0.4}[severity]
    criticality_weight = 0.7 if criticality == "high" else 0.1

    risk_logit = (
        -3.0
        + severity_weight
        + criticality_weight
        + recent_alerts_1h * 0.055
        + error_rate_15m * 4.8
        + max(cpu_p95_30m - 75, 0) * 0.035
        + failed_signins_30m * 0.012
        + max(sql_dtu_max_30m - 80, 0) * 0.04
        + max(vm_heartbeat_gap_min - 10, 0) * 0.055
        + deployment_within_2h * 0.55
        + keyvault_denials_30m * 0.08
    )

    sla_breached = 1 if random.random() < sigmoid(risk_logit) else 0
    opened_at = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 90), minutes=random.randint(0, 1440))

    return {
        "incident_id": f"INC-{index:05d}",
        "opened_at": opened_at.isoformat(),
        "customer": customer,
        "environment": random.choices(["prod", "stage", "dev"], weights=[75, 15, 10])[0],
        "service": service,
        "severity": severity,
        "criticality": criticality,
        "recent_alerts_1h": recent_alerts_1h,
        "error_rate_15m": error_rate_15m,
        "cpu_p95_30m": cpu_p95_30m,
        "failed_signins_30m": failed_signins_30m,
        "sql_dtu_max_30m": sql_dtu_max_30m,
        "vm_heartbeat_gap_min": vm_heartbeat_gap_min,
        "deployment_within_2h": deployment_within_2h,
        "keyvault_denials_30m": keyvault_denials_30m,
        "sla_breached": sla_breached,
    }


def main() -> None:
    random.seed(1004)
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = [generate_row(index) for index in range(1, 751)]

    with RAW_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {RAW_PATH}")


if __name__ == "__main__":
    main()
