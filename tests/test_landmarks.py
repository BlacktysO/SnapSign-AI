import numpy as np
from app.landmarks import normalize_landmarks

def test_normalization_shape_and_wrist_origin():
    pts = np.zeros((21, 3), dtype=np.float32)
    pts[:, 0] = np.linspace(0, 1, 21)
    out = normalize_landmarks(pts)
    assert out.shape == (63,)
    assert np.allclose(out[:3], 0.0)

def test_normalization_is_finite():
    pts = np.random.rand(21, 3).astype(np.float32)
    out = normalize_landmarks(pts)
    assert np.isfinite(out).all()
