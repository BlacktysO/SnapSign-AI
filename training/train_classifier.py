"""Train and evaluate the SnapSign Random Forest classifier."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    ConfusionMatrixDisplay, precision_recall_fscore_support
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "dataset" / "landmarks.csv"
MODEL_PATH = ROOT / "models" / "gesture_classifier.joblib"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)
MODEL_PATH.parent.mkdir(exist_ok=True)


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"{CSV_PATH} not found. Run training/collect_landmarks.py first."
        )

    df = pd.read_csv(CSV_PATH)
    feature_cols = [c for c in df.columns if c.startswith("f")]
    if len(feature_cols) != 63:
        raise ValueError(f"Expected 63 feature columns, found {len(feature_cols)}")

    X = df[feature_cols].astype(np.float32).values
    y = df["label"].astype(str).values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_leaf=1,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ))
    ])

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc = float(accuracy_score(y_test, pred))
    p, r, f1, _ = precision_recall_fscore_support(
        y_test, pred, average="weighted", zero_division=0
    )

    report = classification_report(y_test, pred, zero_division=0)
    (RESULTS / "classification_report.txt").write_text(report, encoding="utf-8")

    metrics = {
        "accuracy": acc,
        "precision_weighted": float(p),
        "recall_weighted": float(r),
        "f1_weighted": float(f1),
        "train_samples": int(len(y_train)),
        "test_samples": int(len(y_test)),
        "classes": sorted(set(y)),
        "feature_count": int(X.shape[1]),
        "random_state": 42,
    }
    (RESULTS / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )

    cm = confusion_matrix(y_test, pred, labels=sorted(set(y)))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=sorted(set(y)))
    fig, ax = plt.subplots(figsize=(10, 8))
    disp.plot(ax=ax, xticks_rotation=45, colorbar=False)
    plt.tight_layout()
    fig.savefig(RESULTS / "confusion_matrix.png", dpi=180)
    plt.close(fig)

    joblib.dump(model, MODEL_PATH)

    print(json.dumps(metrics, indent=2))
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Results saved to: {RESULTS}")


if __name__ == "__main__":
    main()
