# Qualcomm AI Hub / Snapdragon deployment plan

## Why this architecture

SnapSign keeps a stable interface between the hand-perception stage and the custom classifier:

```text
image/frame -> hand landmarks -> normalized vector -> classifier
```

That makes it possible to develop on a normal Windows PC and later replace the hand-perception backend with a Qualcomm AI Hub/QNN-optimized artifact without redesigning the classifier.

## Current AI Hub references

Qualcomm AI Hub currently lists:

- MediaPipe Hand Gesture Recognition
- MediaPipe Hand Detection
- Llama 3.2 1B Instruct
- Llama 3.2 3B Instruct / SSD variants
- MeloTTS-EN

The exact availability/runtime support should be rechecked before final submission because AI Hub model support and job artifacts can change.

## Hand perception

Recommended target for the Snapdragon prototype:

1. MediaPipe hand/palm detector
2. MediaPipe hand landmark detector
3. Optional canned gesture classifier

The custom SnapSign classifier remains separate because the project vocabulary is application-specific.

## Windows / QNN

For supported Snapdragon Windows targets, Qualcomm AI Hub job results can use ONNX Runtime with the QNN execution provider or the Qualcomm AI runtime stack, depending on the model/artifact.

The deployment process should be:

1. Select a supported Snapdragon compute target in AI Hub.
2. Choose/download the compatible model artifact.
3. Verify input/output tensor shapes.
4. Integrate the artifact behind the `HandTracker` interface.
5. Confirm the execution provider is QNN/Qualcomm as appropriate.
6. Measure end-to-end latency on the actual HP Snapdragon PC.
7. Record model/runtime versions in `docs/BENCHMARK_TEMPLATE.md`.

## Important

Do not copy AI Hub benchmark numbers into the project's own benchmark table as if they were measured by SnapSign. AI Hub job metrics are model/job-specific reference measurements. SnapSign's final benchmark must be measured on the actual target system.

## Optional local LLM

For contextual sentence generation, a compatible Qualcomm AI Hub Llama model can be evaluated. The baseline repository intentionally uses a deterministic context engine so the prototype works without a large language model.

A later integration can expose:

```python
generate_sentence(sequence) -> sentence
```

and replace the rule-based implementation with a local LLM while preserving the rest of the application.

## Optional TTS

MeloTTS-EN is listed by Qualcomm AI Hub for Snapdragon X Elite, X Plus 8-Core and X2 Elite targets. The baseline app uses `pyttsx3` for portability; an AI Hub/QNN TTS backend can replace it on the Snapdragon target.
