"""Gesture classifier wrapper."""

from __future__ import annotations

from pathlib import Path
import joblib
import numpy as np


class GestureClassifier:
    def __init__(self, model_path="models/gesture_classifier.joblib"):
        self.model_path = Path(model_path)
        self.model = None
        self.labels = []
        if self.model_path.exists():
            self.model = joblib.load(self.model_path)
            self.labels = list(getattr(self.model, "classes_", []))

    @property
    def ready(self):
        return self.model is not None

    def predict(self, features):
        if not self.ready:
            return "NO_MODEL", 0.0
        x = np.asarray(features, dtype=np.float32).reshape(1, -1)
        pred = self.model.predict(x)[0]
        confidence = 0.0
        if hasattr(self.model, "predict_proba"):
            confidence = float(np.max(self.model.predict_proba(x)[0]))
        return str(pred), confidence
