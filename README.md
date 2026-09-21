# \# SnapSign AI

# 

# \## An On-Device Sign Language Communication Assistant for Snapdragon-Powered PCs

# 

# \*\*SnapSign AI\*\* is a local-first accessibility prototype that converts configurable hand gestures into short contextual messages and optional speech.

# 

# The system uses a webcam to capture hand movements, extracts hand landmarks, classifies gestures using a lightweight Random Forest model, maintains a short gesture sequence, generates contextual text, and optionally converts the resulting message to speech.

# 

# The architecture is designed with \*\*Snapdragon-powered HP PCs\*\* as the target deployment platform, with a planned Qualcomm AI Hub/QNN-optimized hand-perception path.

# 

# > \*\*Important:\*\* The current repository contains a runnable prototype developed and tested on a non-Snapdragon Windows PC. It does \*\*not\*\* claim that the current implementation executes on a Snapdragon NPU. Snapdragon deployment and performance measurements must be validated on the target Snapdragon hardware.

# 

# \---

# 

# \## Key Features

# 

# \* Real-time webcam hand tracking

# \* 21 hand landmarks per detected hand

# \* Landmark normalization for improved position/scale robustness

# \* Custom Random Forest gesture classifier

# \* Configurable gesture vocabulary

# \* Gesture sequence buffer

# \* Context-aware sentence generation

# \* Text-to-speech output

# \* Custom landmark dataset collection

# \* Model training and evaluation scripts

# \* Confusion matrix and classification metrics

# \* Snapdragon / Qualcomm AI Hub deployment path

# \* Modular architecture for replacing the baseline perception stage with an optimized AI Hub/QNN implementation

# 

# \---

# 

# \## System Workflow

# 

# ```text

# &#x20;                   Webcam

# &#x20;                      |

# &#x20;                      v

# &#x20;             Hand Detection

# &#x20;                      |

# &#x20;                      v

# &#x20;            21 Hand Landmarks

# &#x20;                      |

# &#x20;                      v

# &#x20;            Landmark Normalization

# &#x20;                      |

# &#x20;                      v

# &#x20;             63-Feature Vector

# &#x20;                      |

# &#x20;                      v

# &#x20;           Random Forest Classifier

# &#x20;                      |

# &#x20;                      v

# &#x20;             Gesture Sequence

# &#x20;                      |

# &#x20;                      v

# &#x20;              Context Engine

# &#x20;                 /        \\

# &#x20;                v          v

# &#x20;              Text       Speech

# ```

# 

# \---

# 

# \## Current Prototype

# 

# The current implementation uses:

# 

# | Component          | Technology                          |

# | ------------------ | ----------------------------------- |

# | Camera             | OpenCV                              |

# | Hand perception    | MediaPipe                           |

# | Features           | 21 normalized landmarks / 63 values |

# | Classifier         | Random Forest                       |

# | Context generation | Rule-based context engine           |

# | Speech             | Local text-to-speech                |

# | Platform           | Windows / Python                    |

# 

# The classifier operates on normalized hand-landmark coordinates rather than raw camera images. This keeps the custom classification stage lightweight and separates gesture classification from the underlying hand-perception system.

# 

# \---

# 

# \## Gesture Vocabulary

# 

# The current training pipeline supports the following configurable class labels:

# 

# ```text

# HELLO

# YES

# NO

# THANK\_YOU

# HELP

# WATER

# FOOD

# HOME

# STOP

# EMERGENCY

# ```

# 

# These labels are treated as project-specific classes. The repository does \*\*not\*\* claim that the corresponding gesture definitions constitute a standardized ISL vocabulary.

# 

# The vocabulary can be expanded or replaced by collecting additional landmark samples and retraining the classifier.

# 

# \---

# 

# \## Project Structure

# 

# ```text

# SnapSign\_AI/

# │

# ├── app/

# │   ├── main.py

# │   ├── classifier.py

# │   ├── context\_engine.py

# │   ├── landmarks.py

# │   ├── mediapipe\_tracker.py

# │   ├── speech.py

# │   └── \_\_init\_\_.py

# │

# ├── dataset/

# │   ├── landmarks.csv

# │   └── README.md

# │

# ├── docs/

# │   ├── ARCHITECTURE.md

# │   └── BENCHMARK\_TEMPLATE.md

# │

# ├── models/

# │   └── gesture\_classifier.joblib

# │

# ├── qualcomm/

# │   └── AI\_HUB\_DEPLOYMENT.md

# │

# ├── results/

# │   ├── metrics.json

# │   ├── classification\_report.txt

# │   └── confusion\_matrix.png

# │

# ├── tests/

# │   └── test\_landmarks.py

# │

# ├── training/

# │   ├── collect\_landmarks.py

# │   └── train\_classifier.py

# │

# ├── requirements.txt

# ├── LICENSE

# └── README.md

# ```

# 

# \---

# 

# \# Installation

# 

# \## Requirements

# 

# Recommended environment:

# 

# \* Windows 10/11

# \* Python 3.11

# \* Webcam

# 

# Create a virtual environment:

# 

# ```powershell

# py -3.11 -m venv .venv

# ```

# 

# Activate it:

# 

# ```powershell

# .venv\\Scripts\\activate

# ```

# 

# Install dependencies:

# 

# ```powershell

# python -m pip install --upgrade pip

# pip install -r requirements.txt

# ```

# 

# \---

# 

# \# Collect Training Data

# 

# Run:

# 

# ```powershell

# python training\\collect\_landmarks.py

# ```

# 

# The collector captures hand landmarks from the webcam and stores normalized landmark vectors in:

# 

# ```text

# dataset/landmarks.csv

# ```

# 

# For a more robust dataset, use:

# 

# \* multiple recording sessions

# \* different hand positions

# \* different distances from the camera

# \* different backgrounds

# \* left/right hands where applicable

# \* approximately 500–1000 samples per class as a starting target

# 

# \---

# 

# \# Train the Gesture Classifier

# 

# Run:

# 

# ```powershell

# python training\\train\_classifier.py

# ```

# 

# The training pipeline generates:

# 

# ```text

# models/gesture\_classifier.joblib

# results/metrics.json

# results/classification\_report.txt

# results/confusion\_matrix.png

# ```

# 

# The trained model is a lightweight Random Forest classifier operating on the normalized landmark features.

# 

# \---

# 

# \# Run SnapSign AI

# 

# Start the application with:

# 

# ```powershell

# python app\\main.py

# ```

# 

# The application provides:

# 

# \* live camera feed

# \* hand tracking

# \* predicted gesture

# \* confidence value

# \* gesture sequence

# \* generated message

# \* optional speech output

# \* application status information

# 

# \### Keyboard Controls

# 

# ```text

# Q / ESC  Exit

# R        Reset gesture sequence

# S        Speak current sentence

# M        Toggle speech

# ```

# 

# \---

# 

# \# Snapdragon + Qualcomm AI Hub Integration

# 

# SnapSign AI separates the application layer from the hand-perception layer so that the baseline MediaPipe implementation can be replaced or complemented by an optimized deployment path.

# 

# Qualcomm AI Hub currently lists \*\*MediaPipe Hand Gesture Recognition\*\* and \*\*MediaPipe Hand Detection\*\* with Snapdragon X Elite, Snapdragon X Plus 8-Core, and Snapdragon X2 Elite targets. The gesture-recognition pipeline includes hand detection, 21 hand landmarks, and gesture classification.

# 

# Qualcomm AI Hub also provides Windows 11 profiling jobs showing QNN/NPU execution for components of the MediaPipe hand pipeline on Snapdragon X Elite and X2 Elite target devices. These are Qualcomm AI Hub profiling results and are \*\*not measurements of the current SnapSign AI prototype\*\*.

# 

# \### Intended Competition Architecture

# 

# ```text

# &#x20;             HP Snapdragon PC

# &#x20;                     |

# &#x20;                     v

# &#x20;                  Webcam

# &#x20;                     |

# &#x20;                     v

# &#x20;       Qualcomm AI Hub / QNN

# &#x20;         Optimized Perception

# &#x20;                     |

# &#x20;                     v

# &#x20;               21 Landmarks

# &#x20;                     |

# &#x20;                     v

# &#x20;         SnapSign Gesture Classifier

# &#x20;                     |

# &#x20;                     v

# &#x20;              Context Engine

# &#x20;                 /       \\

# &#x20;                v         v

# &#x20;              Text      TTS

# ```

# 

# The modular design allows the application-level gesture vocabulary and contextual processing to remain independent from the underlying hardware-optimized perception implementation.

# 

# \---

# 

# \# Snapdragon Deployment Plan

# 

# The current repository provides the baseline prototype and the planned Snapdragon deployment path.

# 

# Before making hardware-specific performance claims, the following should be completed on an actual Snapdragon-powered HP PC:

# 

# 1\. Select the appropriate Qualcomm AI Hub artifact.

# 2\. Integrate the optimized hand-perception model.

# 3\. Verify QNN/NPU execution.

# 4\. Measure end-to-end latency.

# 5\. Measure sustained frame rate.

# 6\. Record CPU/NPU utilization where available.

# 7\. Record exact model, runtime, and operating-system versions.

# 8\. Compare baseline and Snapdragon-target execution.

# 9\. Add measured results to:

# 

# ```text

# docs/BENCHMARK\_TEMPLATE.md

# ```

# 

# \---

# 

# \# Evaluation

# 

# The project can be evaluated using:

# 

# \### Recognition

# 

# \* Accuracy

# \* Precision

# \* Recall

# \* F1-score

# \* Confusion matrix

# 

# \### Runtime

# 

# \* End-to-end latency

# \* Frames per second

# \* Model inference time

# \* Startup time

# 

# \### Deployment

# 

# \* CPU/NPU execution

# \* Memory usage

# \* Responsiveness

# \* Stability during continuous operation

# 

# \### Accessibility

# 

# \* Recognition consistency

# \* Ease of interaction

# \* Speech output responsiveness

# \* Configurability of the gesture vocabulary

# 

# No Snapdragon performance value is reported in this repository unless it has been measured on the corresponding target hardware.

# 

# \---

# 

# \# Why Snapdragon?

# 

# SnapSign AI is designed around a local-first workflow where camera data can be processed on the user's computer rather than requiring continuous cloud transmission.

# 

# A Snapdragon-powered PC provides a natural target for exploring:

# 

# \* on-device AI inference

# \* hardware-accelerated model execution

# \* low-latency computer vision

# \* privacy-oriented local processing

# \* efficient accessibility applications

# 

# The project therefore separates the \*\*application logic\*\* from the \*\*hardware-specific AI inference layer\*\*, making the system suitable for future optimization using Qualcomm AI Hub and QNN.

# 

# \---

# 

# \# Privacy

# 

# The baseline application processes webcam frames locally.

# 

# The prototype does not require a remote server for its basic gesture-recognition workflow.

# 

# Users should still review the behavior of any future cloud-connected components before deployment.

# 

# \---

# 

# \# Research and Development Status

# 

# \*\*Current status:\*\*

# 

# ```text

# \[✓] Webcam capture

# \[✓] Hand landmark extraction

# \[✓] Landmark normalization

# \[✓] Custom gesture dataset

# \[✓] Random Forest classifier

# \[✓] Gesture sequence handling

# \[✓] Context generation

# \[✓] Text-to-speech

# \[✓] Evaluation outputs

# \[✓] Snapdragon deployment architecture

# \[✓] Qualcomm AI Hub deployment documentation

# \[ ] Snapdragon hardware validation

# \[ ] QNN/NPU benchmark measurements

# ```

# 

# The final two items require access to compatible Snapdragon hardware and are intentionally not represented as completed.

# 

# \---

# 

# \# Future Development

# 

# Potential extensions include:

# 

# \* Dynamic gesture recognition

# \* Larger configurable vocabularies

# \* Continuous sentence formation

# \* Two-hand gesture support

# \* Personalized gesture profiles

# \* Multilingual speech output

# \* Speech-to-sign interaction

# \* Qualcomm AI Hub optimized language models

# \* Fully hardware-accelerated Snapdragon inference

# \* Quantized model deployment

# \* On-device language understanding

# 

# \---

# 

# \# License and Model Notes

# 

# Application code may be released under the MIT License.

# 

# Third-party libraries, datasets, models, and Qualcomm AI Hub artifacts retain their respective licenses and terms.

# 

# See:

# 

# ```text

# LICENSE

# qualcomm/AI\_HUB\_DEPLOYMENT.md

# ```

# 

# before redistributing third-party model artifacts.

# 

# \---

# 

# \## Project Summary

# 

# \*\*SnapSign AI\*\* demonstrates a modular, local-first approach to accessible sign-language communication.

# 

# The current prototype combines computer vision, lightweight machine learning, contextual processing, and speech synthesis while providing a defined path toward Snapdragon-optimized deployment.

# 

# The project is intended to explore how an accessibility-focused AI application can transition from a conventional Windows prototype to an optimized \*\*Snapdragon + Qualcomm AI Hub\*\* implementation.



