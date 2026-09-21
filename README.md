# SnapSign AI

**An On-Device Sign Language Communication Assistant for Snapdragon-Powered PCs**

SnapSign AI is a local-first accessibility prototype that converts configurable hand gestures into short contextual messages and optional speech.

The system uses a webcam to capture hand movements, extracts hand landmarks, classifies gestures using a lightweight Random Forest model, maintains a short gesture sequence, generates contextual text, and optionally converts the result to speech.

The architecture is designed with Snapdragon-powered HP PCs as the target deployment platform, with a planned Qualcomm AI Hub/QNN-optimized hand-perception path.

## Features

- Real-time webcam hand tracking
- 21 hand landmarks per detected hand
- Landmark normalization
- Custom Random Forest gesture classifier
- Configurable gesture vocabulary
- Gesture sequence processing
- Context-aware sentence generation
- Text-to-speech output
- Custom landmark dataset collection
- Model training and evaluation
- Confusion matrix and classification metrics
- Snapdragon / Qualcomm AI Hub deployment path

## How It Works

```text
Webcam
   |
   v
Hand Detection
   |
   v
21 Hand Landmarks
   |
   v
Landmark Normalization
   |
   v
63-Feature Vector
   |
   v
Random Forest Classifier
   |
   v
Gesture Sequence
   |
   v
Context Engine
   |
   +----> Text
   |
   +----> Speech
