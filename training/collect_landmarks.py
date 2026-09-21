"""Collect normalized hand landmark samples from a webcam."""

from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.mediapipe_tracker import HandTracker
from app.landmarks import normalize_landmarks

LABELS = [
    "HELLO", "YES", "NO", "THANK_YOU", "HELP",
    "WATER", "FOOD", "HOME", "STOP", "EMERGENCY"
]

CSV_PATH = ROOT / "dataset" / "landmarks.csv"
HEADER = ["label", "handedness"] + [f"f{i}" for i in range(63)]


def append_sample(label, handedness, vector):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    new_file = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(HEADER)
        writer.writerow([label, handedness, *vector.tolist()])


def main():
    print("SnapSign landmark collector")
    print("Labels:", ", ".join(LABELS))
    label = input("Enter label: ").strip().upper()
    if label not in LABELS:
        raise ValueError(f"Unknown label. Choose one of: {LABELS}")

    target = int(input("Samples to collect [500]: ") or "500")
    warmup = float(input("Warm-up seconds [2]: ") or "2")

    tracker = HandTracker()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    count = 0
    start = time.time()

    try:
        while count < target:
            ok, frame = cap.read()
            if not ok:
                continue
            frame = cv2.flip(frame, 1)

            result = tracker.process(frame)
            tracker.draw(frame, result)
            landmarks = tracker.result_to_array(result)

            elapsed = time.time() - start
            if elapsed >= warmup and landmarks is not None:
                vec = normalize_landmarks(landmarks)
                append_sample(label, "UNKNOWN", vec)
                count += 1

            cv2.putText(frame, f"Collecting: {label}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            cv2.putText(frame, f"{count}/{target}", (20, 75),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(frame, "Hold gesture steadily | Q to stop", (20, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 1)
            cv2.imshow("SnapSign Dataset Collector", frame)

            if cv2.waitKey(1) & 0xFF in (27, ord("q")):
                break
    finally:
        cap.release()
        tracker.close()
        cv2.destroyAllWindows()

    print(f"Saved {count} samples to {CSV_PATH}")


if __name__ == "__main__":
    main()
