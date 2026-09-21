"""Offline text-to-speech wrapper."""

from __future__ import annotations

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


class Speaker:
    def __init__(self):
        self.engine = None
        if pyttsx3 is not None:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 165)
            except Exception:
                self.engine = None

    @property
    def available(self):
        return self.engine is not None

    def speak(self, text: str):
        if not text or not self.engine:
            return False
        self.engine.say(text)
        self.engine.runAndWait()
        return True
