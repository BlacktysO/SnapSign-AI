from __future__ import annotations

import sys
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.mediapipe_tracker import HandTracker
from app.landmarks import normalize_landmarks
from app.classifier import GestureClassifier
from app.context_engine import generate_sentence
from app.speech import Speaker


# ============================================================
# CONFIGURATION
# ============================================================

WINDOW_NAME = "SnapSign AI"
MODEL_PATH = ROOT / "models" / "gesture_classifier.joblib"

CAMERA_WIDTH = 960
CAMERA_HEIGHT = 540


# ============================================================
# DRAWING FUNCTIONS
# ============================================================

def draw_panel(img, x1, y1, x2, y2, fill=(25, 28, 35)):
    cv2.rectangle(
        img,
        (x1, y1),
        (x2, y2),
        fill,
        -1
    )

    cv2.rectangle(
        img,
        (x1, y1),
        (x2, y2),
        (65, 70, 80),
        1
    )


def put_text(
    img,
    text,
    position,
    size=0.6,
    color=(235, 235, 235),
    thickness=1
):
    cv2.putText(
        img,
        str(text),
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        size,
        color,
        thickness,
        cv2.LINE_AA
    )


def draw_header(canvas):
    draw_panel(
        canvas,
        0,
        0,
        canvas.shape[1],
        78,
        (17, 20, 27)
    )

    put_text(
        canvas,
        "SNAPSIGN AI",
        (30, 35),
        0.9,
        (255, 255, 255),
        2
    )

    put_text(
        canvas,
        "On-Device Sign Language Communication Assistant",
        (30, 61),
        0.43,
        (165, 175, 190),
        1
    )

    # AI status
    cv2.circle(
        canvas,
        (canvas.shape[1] - 180, 30),
        7,
        (70, 210, 120),
        -1
    )

    put_text(
        canvas,
        "AI ENGINE ACTIVE",
        (canvas.shape[1] - 162, 36),
        0.43,
        (210, 220, 215),
        1
    )


def draw_camera_area(canvas, frame):
    h, w = frame.shape[:2]

    x1 = 25
    y1 = 100
    x2 = 665
    y2 = 555

    camera = cv2.resize(
        frame,
        (x2 - x1, y2 - y1)
    )

    canvas[y1:y2, x1:x2] = camera

    cv2.rectangle(
        canvas,
        (x1, y1),
        (x2, y2),
        (85, 95, 110),
        2
    )

    put_text(
        canvas,
        "LIVE CAMERA",
        (x1 + 15, y1 + 28),
        0.5,
        (255, 255, 255),
        1
    )


def draw_info_panel(
    canvas,
    label,
    confidence,
    sequence,
    sentence,
    latency,
    speech_on
):

    x1 = 690
    x2 = canvas.shape[1] - 25

    # Gesture panel
    draw_panel(
        canvas,
        x1,
        100,
        x2,
        225
    )

    put_text(
        canvas,
        "DETECTED GESTURE",
        (x1 + 20, 130),
        0.43,
        (145, 155, 170),
        1
    )

    put_text(
        canvas,
        label,
        (x1 + 20, 175),
        0.95,
        (255, 255, 255),
        2
    )

    put_text(
        canvas,
        f"Confidence  {confidence * 100:.1f}%",
        (x1 + 20, 205),
        0.42,
        (160, 205, 180),
        1
    )

    # Sequence panel
    draw_panel(
        canvas,
        x1,
        240,
        x2,
        335
    )

    put_text(
        canvas,
        "GESTURE SEQUENCE",
        (x1 + 20, 267),
        0.43,
        (145, 155, 170),
        1
    )

    seq_text = "  +  ".join(sequence) if sequence else "Waiting..."

    put_text(
        canvas,
        seq_text[:38],
        (x1 + 20, 305),
        0.52,
        (240, 240, 240),
        1
    )

    # Sentence panel
    draw_panel(
        canvas,
        x1,
        350,
        x2,
        470
    )

    put_text(
        canvas,
        "GENERATED MESSAGE",
        (x1 + 20, 378),
        0.43,
        (145, 155, 170),
        1
    )

    display_sentence = (
        sentence[:42]
        if sentence
        else "Show a gesture to begin..."
    )

    put_text(
        canvas,
        display_sentence,
        (x1 + 20, 420),
        0.52,
        (255, 255, 255),
        1
    )

    # Status panel
    draw_panel(
        canvas,
        x1,
        485,
        x2,
        555
    )

    put_text(
        canvas,
        f"Latency: {latency:.1f} ms",
        (x1 + 20, 515),
        0.42,
        (175, 185, 200),
        1
    )

    put_text(
        canvas,
        f"Speech: {'ON' if speech_on else 'OFF'}",
        (x1 + 170, 515),
        0.42,
        (175, 185, 200),
        1
    )


def draw_footer(canvas):

    y = canvas.shape[0] - 30

    put_text(
        canvas,
        "R  Reset     S  Speak     M  Speech     Q / ESC  Exit",
        (30, y),
        0.43,
        (160, 170, 185),
        1
    )

    put_text(
        canvas,
        "Snapdragon Target • Qualcomm AI Hub Ready",
        (canvas.shape[1] - 355, y),
        0.38,
        (120, 170, 145),
        1
    )


# ============================================================
# MAIN
# ============================================================

def main():

    tracker = HandTracker()

    classifier = GestureClassifier(
        MODEL_PATH
    )

    speaker = Speaker()

    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Webcam could not be opened.")
        return

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        CAMERA_WIDTH
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        CAMERA_HEIGHT
    )

    sequence = deque(maxlen=5)

    last_label = None
    stable_count = 0
    last_added = 0

    speech_on = True

    print("======================================")
    print("           SNAP SIGN AI")
    print("======================================")
    print("Gesture model:", classifier.ready)
    print("Speech:", speaker.available)
    print()
    print("Application started.")

    try:

        while True:

            start = time.perf_counter()

            ok, frame = cap.read()

            if not ok:
                continue

            frame = cv2.flip(
                frame,
                1
            )

            # ------------------------------------------------
            # HAND TRACKING
            # ------------------------------------------------

            result = tracker.process(frame)

            tracker.draw(
                frame,
                result
            )

            label = "NO HAND"
            confidence = 0

            landmarks = tracker.result_to_array(
                result
            )

            # ------------------------------------------------
            # CLASSIFICATION
            # ------------------------------------------------

            if landmarks is not None:

                features = normalize_landmarks(
                    landmarks
                )

                label, confidence = classifier.predict(
                    features
                )

                if label == last_label:

                    stable_count += 1

                else:

                    last_label = label
                    stable_count = 1

                now = time.time()

                if (
                    stable_count >= 8
                    and confidence >= 0.55
                    and now - last_added > 1.2
                    and label not in (
                        "NO_MODEL",
                        "NO HAND"
                    )
                ):

                    sequence.append(label)

                    last_added = now

                    stable_count = 0

            # ------------------------------------------------
            # SENTENCE
            # ------------------------------------------------

            sentence = generate_sentence(
                list(sequence)
            )

            latency = (
                time.perf_counter() - start
            ) * 1000

            # ------------------------------------------------
            # CREATE UI
            # ------------------------------------------------

            canvas = np.zeros(
                (590, 1280, 3),
                dtype=np.uint8
            )

            draw_header(
                canvas
            )

            draw_camera_area(
                canvas,
                frame
            )

            draw_info_panel(
                canvas,
                label,
                confidence,
                list(sequence),
                sentence,
                latency,
                speech_on
            )

            draw_footer(
                canvas
            )

            cv2.imshow(
                WINDOW_NAME,
                canvas
            )

            key = cv2.waitKey(1) & 0xFF

            # ------------------------------------------------
            # CONTROLS
            # ------------------------------------------------

            if key in (
                ord("q"),
                27
            ):
                break

            elif key == ord("r"):

                sequence.clear()

                last_label = None
                stable_count = 0
                last_added = 0

                print("Sequence reset.")

            elif key == ord("m"):

                speech_on = not speech_on

                print(
                    "Speech:",
                    "ON" if speech_on else "OFF"
                )

            elif key == ord("s"):

                if (
                    speech_on
                    and sentence
                ):

                    print(
                        "Speaking:",
                        sentence
                    )

                    speaker.speak(
                        sentence
                    )

    finally:

        cap.release()

        tracker.close()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()