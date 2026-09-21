"""Small deterministic context engine.

This keeps the baseline project offline and dependency-light.
A compatible local LLM can replace this layer later.
"""

from __future__ import annotations

TEMPLATES = {
    ("HELP",): "I need help, please.",
    ("WATER",): "I need some water, please.",
    ("FOOD",): "I would like some food, please.",
    ("HOME",): "I want to go home.",
    ("THANK_YOU",): "Thank you.",
    ("HELLO",): "Hello.",
    ("YES",): "Yes.",
    ("NO",): "No.",
    ("STOP",): "Please stop.",
    ("EMERGENCY",): "This is an emergency. Please help.",
    ("HELP", "WATER"): "I need some water, please.",
    ("HELP", "FOOD"): "I need some food, please.",
    ("I", "NEED", "WATER"): "I need some water, please.",
}


def generate_sentence(sequence):
    seq = tuple(sequence)
    if not seq:
        return ""
    if seq in TEMPLATES:
        return TEMPLATES[seq]

    # Simple fallback that avoids pretending to be an LLM.
    readable = " ".join(x.replace("_", " ").title() for x in seq)
    return readable + "."
