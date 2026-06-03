"""Train a small logistic regression model for SLA breach prediction.

The implementation intentionally uses only the Python standard library so the
portfolio can be cloned and executed without dependency setup.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "synthetic_incidents.csv"
MODEL_PATH = ROOT / "ml" / "sla_model.json"
EVAL_PATH = ROOT / "ml" / "evaluation.md"

NUMERIC_FEATURES = [
    "recent_alerts_1h",
    "error_rate_15m",
    "cpu_p95_30m",
    "failed_signins_30m",
    "sql_dtu_max_30m",
    "vm_heartbeat_gap_min",
    "deployment_within_2h",
    "keyvault_denials_30m",
]

CATEGORICAL_FEATURES = ["service", "severity", "criticality", "environment"]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


def sigmoid(value: float) -> float:
    if value < -40:
        return 0.0
    if value > 40:
        return 1.0
    return 1.0 / (1.0 + math.exp(-value))


def build_vocab(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    return {
        name: sorted({row[name] for row in rows})
        for name in CATEGORICAL_FEATURES
    }


def numeric_stats(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}
    for name in NUMERIC_FEATURES:
        values = [float(row[name]) for row in rows]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        stats[name] = {"mean": mean, "std": math.sqrt(variance) or 1.0}
    return stats


def vectorize(row: dict[str, str], stats: dict[str, dict[str, float]], vocab: dict[str, list[str]]) -> list[float]:
    values = [1.0]
    for name in NUMERIC_FEATURES:
        value = float(row[name])
        values.append((value - stats[name]["mean"]) / stats[name]["std"])
    for name in CATEGORICAL_FEATURES:
        for category in vocab[name]:
            values.append(1.0 if row[name] == category else 0.0)
    return values


def train(xs: list[list[float]], ys: list[int], epochs: int = 700, learning_rate: float = 0.08) -> list[float]:
    weights = [0.0 for _ in xs[0]]
    for _ in range(epochs):
        gradients = [0.0 for _ in weights]
        for x_values, target in zip(xs, ys):
            prediction = sigmoid(sum(weight * value for weight, value in zip(weights, x_values)))
            error = prediction - target
            for index, value in enumerate(x_values):
                gradients[index] += error * value
        for index in range(len(weights)):
            weights[index] -= learning_rate * gradients[index] / len(xs)
    return weights


def evaluate(xs: list[list[float]], ys: list[int], weights: list[float]) -> dict[str, float]:
    tp = fp = tn = fn = 0
    for x_values, target in zip(xs, ys):
        probability = sigmoid(sum(weight * value for weight, value in zip(weights, x_values)))
        predicted = 1 if probability >= 0.5 else 0
        if predicted == 1 and target == 1:
            tp += 1
        elif predicted == 1 and target == 0:
            fp += 1
        elif predicted == 0 and target == 0:
            tn += 1
        else:
            fn += 1

    accuracy = (tp + tn) / max(tp + fp + tn + fn, 1)
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 0.0001)
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1, "tp": tp, "fp": fp, "tn": tn, "fn": fn}


def main() -> None:
    if not RAW_PATH.exists():
        raise SystemExit("Run scripts/generate_synthetic_incidents.py first.")

    rows = read_rows(RAW_PATH)
    split = int(len(rows) * 0.8)
    train_rows = rows[:split]
    test_rows = rows[split:]

    stats = numeric_stats(train_rows)
    vocab = build_vocab(train_rows)
    x_train = [vectorize(row, stats, vocab) for row in train_rows]
    y_train = [int(row["sla_breached"]) for row in train_rows]
    x_test = [vectorize(row, stats, vocab) for row in test_rows]
    y_test = [int(row["sla_breached"]) for row in test_rows]

    weights = train(x_train, y_train)
    metrics = evaluate(x_test, y_test, weights)

    model = {
        "model_type": "standard-library-logistic-regression",
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "stats": stats,
        "vocab": vocab,
        "weights": weights,
        "threshold": 0.5,
        "metrics": metrics,
    }

    MODEL_PATH.write_text(json.dumps(model, indent=2), encoding="utf-8")
    EVAL_PATH.write_text(
        "\n".join(
            [
                "# SLA Breach Model Evaluation",
                "",
                "| Metric | Value |",
                "| --- | ---: |",
                f"| Accuracy | {metrics['accuracy']:.3f} |",
                f"| Precision | {metrics['precision']:.3f} |",
                f"| Recall | {metrics['recall']:.3f} |",
                f"| F1 | {metrics['f1']:.3f} |",
                "",
                "## Confusion Matrix",
                "",
                f"- True positives: {metrics['tp']}",
                f"- False positives: {metrics['fp']}",
                f"- True negatives: {metrics['tn']}",
                f"- False negatives: {metrics['fn']}",
                "",
                "The model is intentionally simple. Its purpose is to demonstrate feature engineering and operations-aware risk scoring, not to replace human incident triage.",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote model to {MODEL_PATH}")
    print(f"Wrote evaluation to {EVAL_PATH}")


if __name__ == "__main__":
    main()
