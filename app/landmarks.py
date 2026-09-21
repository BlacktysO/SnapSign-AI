"""Landmark preprocessing utilities for SnapSign AI."""

from __future__ import annotations

import numpy as np


def normalize_landmarks(landmarks: np.ndarray) -> np.ndarray:
    """
    Normalize 21 hand landmarks.

    Input:
        shape (21, 3), coordinates x/y/z.
    Output:
        shape (63,), centered at the wrist and scaled by the maximum
        2D distance from the wrist. This reduces sensitivity to hand
        position and approximate scale.
    """
    pts = np.asarray(landmarks, dtype=np.float32).reshape(21, 3)
    origin = pts[0].copy()
    pts = pts - origin

    distances = np.linalg.norm(pts[:, :2], axis=1)
    scale = float(np.max(distances))
    if scale < 1e-6:
        scale = 1.0

    pts /= scale
    return pts.reshape(-1).astype(np.float32)


def vector_to_matrix(vector: np.ndarray) -> np.ndarray:
    return np.asarray(vector, dtype=np.float32).reshape(21, 3)
