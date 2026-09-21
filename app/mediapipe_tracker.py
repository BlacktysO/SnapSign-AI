"""MediaPipe hand landmark tracker.

This is the portable development backend. For Snapdragon deployment,
replace this stage with the selected Qualcomm AI Hub/QNN artifact while
keeping the normalized landmark interface unchanged.
"""

from __future__ import annotations

import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    def __init__(self, max_num_hands: int = 1, min_detection_confidence: float = 0.55,
                 min_tracking_confidence: float = 0.55):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def process(self, frame_bgr):
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        result = self.hands.process(rgb)
        rgb.flags.writeable = True
        return result

    def draw(self, frame_bgr, result):
        if not result.multi_hand_landmarks:
            return
        for hand_landmarks in result.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(
                frame_bgr,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
            )

    @staticmethod
    def result_to_array(result, index=0):
        if not result.multi_hand_landmarks:
            return None
        hand = result.multi_hand_landmarks[index]
        return np.array([[p.x, p.y, p.z] for p in hand.landmark], dtype=np.float32)

    def close(self):
        self.hands.close()
