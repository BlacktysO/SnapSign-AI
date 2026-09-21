# Dataset

This folder is intentionally kept free of personal images.

SnapSign stores **hand landmark vectors**, not raw camera frames, by default.

Expected CSV schema:

```text
label,handedness,hand_x1,hand_y1,hand_z1,...,hand_x21,hand_y21,hand_z21
```

There are 63 numeric landmark features per hand.

## Recommended collection protocol

For each class:

- 500-1000 samples minimum
- collect over multiple sessions
- vary lighting and distance
- vary background
- include natural small movements
- keep train/validation/test sessions separate when possible

Do not publish photographs or videos of other people without appropriate permission.
