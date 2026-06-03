"""Score incidents with the trained SLA breach model."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "synthetic_incidents.csv"
MODEL_PATH = ROOT / "ml" / "sla_model.json"
OUTPUT_PATH = ROOT / "data" / "processed" / "scored_incidents.csv"


def sigmoid(value: float) -> float:
    if value < -40:
        return 0.0
    if value > 40:
        return 1.0
    return 1.0 / (1.0 + math.exp(-value))


def vectorize(row: dict[str, str], model: dict) -> list[float]:
    values = [1.0]
    for name in model["numeric_features"]:
        value = float(row[name])
        stat = model["stats"][name]
        values.append((value - stat["mean"]) / stat["std"])
    for name in model["categorical_features"]:
        for category in model["vocab"][name]:
            values.append(1.0 if row[name] == category else 0.0)
    return values


def main() -> None:
    if not MODEL_PATH.exists():
        raise SystemExit("Run ml/train_sla_model.py first.")

    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(RAW_PATH.open(encoding="utf-8")))
    scored_rows = []

    for row in rows:
        x_values = vectorize(row, model)
        probability = sigmoid(sum(weight * value for weight, value in zip(model["weights"], x_values)))
        row["sla_breach_probability"] = f"{probability:.4f}"
        row["risk_band"] = "high" if probability >= 0.7 else "medium" if probability >= 0.35 else "low"
        scored_rows.append(row)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(scored_rows[0].keys()))
        writer.writeheader()
        writer.writerows(scored_rows)

    print(f"Wrote {len(scored_rows)} scored incidents to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
