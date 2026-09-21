# SnapSign AI

**An On-Device Sign Language Communication Assistant for Snapdragon-Powered PCs**

SnapSign AI is a research/prototype application designed around a local-first computer-vision pipeline. It uses a webcam to extract hand landmarks, classifies a configurable gesture vocabulary with a lightweight Random Forest model, builds short contextual sentences from recognized gestures, and can speak the result.

The project is designed for eventual optimization/deployment on Snapdragon-powered HP PCs using Qualcomm AI Hub-compatible models and Qualcomm's supported Windows AI runtimes.

> **Important:** This repository is a prototype. It does not claim Snapdragon/NPU execution on a non-Snapdragon computer. Snapdragon performance numbers must be measured on the target hardware before being reported as project results.

## Features

- Real-time webcam hand tracking
- 21 hand landmarks per detected hand
- Landmark normalization for position/scale robustness
- Custom Random Forest gesture classifier
- Gesture sequence buffer
- Rule-based contextual sentence generation
- Text-to-speech
- Custom gesture data collection
- Training/evaluation scripts
- Confusion matrix and metrics export
- Snapdragon / Qualcomm AI Hub deployment notes
- Optional architecture for replacing local hand perception with AI Hub/QNN optimized models

## Prototype workflow

```text
Webcam
  |
  v
MediaPipe hand landmarks
  |
  v
Normalized 63-feature vector
  |
  v
Random Forest
  |
  v
Gesture sequence
  |
  v
Context engine
  |
  +--> Text
  |
  +--> Text-to-speech
```

## Current prototype vocabulary

The training pipeline supports these class names:

- HELLO
- YES
- NO
- THANK_YOU
- HELP
- WATER
- FOOD
- HOME
- STOP
- EMERGENCY

**Do not claim these are standardized ISL signs until each gesture definition has been validated against a documented sign-language source.** The project intentionally keeps the labels configurable.

## Setup

### 1. Recommended environment

Windows 10/11, Python 3.11.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Collect landmark data

```powershell
python training\collect_landmarks.py
```

Choose a label and hold the corresponding gesture in front of the camera. The collector saves normalized landmark vectors to `dataset/landmarks.csv`.

Recommended target:

- 10 classes
- 500-1000 samples/class
- multiple recording sessions
- different distances/backgrounds
- left/right hands where applicable

### 3. Train

```powershell
python training\train_classifier.py
```

Outputs:

```text
models/gesture_classifier.joblib
results/metrics.json
results/classification_report.txt
results/confusion_matrix.png
```

### 4. Run

```powershell
python app\main.py
```

The application opens a camera window with:

- live hand landmarks
- predicted gesture
- confidence
- recent gesture sequence
- generated sentence
- optional speech output

### 5. Keyboard controls

```text
Q / ESC  Exit
R        Reset sequence
S        Speak current sentence
M        Toggle speech
```

## Qualcomm / Snapdragon deployment

The Snapdragon-specific integration is intentionally separated from the baseline prototype.

Qualcomm AI Hub currently lists MediaPipe Hand Gesture Recognition and MediaPipe Hand Detection for Snapdragon X Elite, X Plus 8-Core and X2 Elite compute targets. AI Hub also provides recent Windows 11 Snapdragon X Elite profiling jobs for the hand-landmark, palm-detection and canned-gesture components using Qualcomm/QNN execution. See `qualcomm/AI_HUB_DEPLOYMENT.md`.

The intended competition architecture is:

```text
HP Snapdragon PC
       |
       v
Camera
       |
       v
AI Hub / QNN optimized hand perception
       |
       v
21 landmarks
       |
       v
Custom SnapSign classifier
       |
       v
Context engine
       |
       +----> Text
       |
       +----> TTS
```

## Project status

The repository contains a runnable local prototype plus a Snapdragon deployment path. The following should be completed on the actual target device before final claims are made:

1. Deploy/replace the hand perception stage with the selected Qualcomm AI Hub artifact.
2. Verify QNN/NPU execution on the HP Snapdragon PC.
3. Measure end-to-end latency and frame rate.
4. Record the exact model/runtime versions.
5. Add measured benchmark results to `docs/BENCHMARK_TEMPLATE.md`.

## License and model notes

Application code in this repository can be released under MIT. Third-party models and packages retain their own licenses. See `LICENSE` and the Qualcomm deployment notes before redistributing model files.
