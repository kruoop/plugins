# Local model recipes and observed pitfalls

## Tested baseline, 2026-09-07

This stack ran on Apple M5 Max with 48 GiB unified memory. Versions are a reproducible baseline, not a request to upgrade unrelated environments or a hardware minimum. Recheck installed versions and model compatibility before reuse. Keep incompatible Transformers generations in separate virtual environments; retain dependency freezes and model revisions with each project's run.

| Component | Tested identity / runtime |
|---|---|
| Qwen primary | `mlx-community/Qwen3-ASR-1.7B-bf16`, revision `e1f6c266914abc5a46e8756e02580f834a6cf8a7`; Apache-2.0; 707 tensors verified BF16 |
| Qwen environment | Python 3.12.14, mlx-audio 0.5.1, MLX 0.32.2, Transformers 5.16.1, NumPy 2.5.3 |
| Whisper check | `mlx-community/whisper-large-v3-turbo`, revision `a4aaeec0636e6fef84abdcbe3544cb2bf7e9f6fb`; mlx-whisper 0.4.3, MLX 0.32.2 |
| Optional Thai Whisper | `biodatlab/whisper-th-large-v3-combined`, revision `ba7197f618400e41b4826c18b2f48e0bc45ed3ca`; weights Apache-2.0; code MIT |
| Thai Whisper / CTC environment | Python 3.12.14, PyTorch 2.14.0, Transformers 4.57.1; Thai Whisper used MPS FP16, CTC used MPS FP32 |
| Typhoon CTC head | `typhoon-ai/typhoon-whisper-large-v3-ctc`, revision `a75e6fcefc33ecec609aca71a5daef74a819b21d`; Apache-2.0 |
| Matching Typhoon encoder | `typhoon-ai/typhoon-whisper-large-v3`, revision `748e8a418697d5920e62bced10590072dce90da5`; MIT |
| VAD | Local Silero via faster-whisper 1.2.1 / ONNX Runtime 1.29.0 |

Model downloads require network access; inference does not need an API key or media upload. Download pinned safetensors/config/tokenizer files from the model repositories, verify hashes where provided, and record the local snapshot path. Do not load pickle training artifacts or execute unaudited remote Python just to get weights. Inspect model-specific implementation code before using it. If Hugging Face Xet stalls, ordinary HTTPS with `HF_HUB_DISABLE_XET=1` was a working fallback.

After downloads, run inference with:

```text
HF_HUB_OFFLINE=1
TRANSFORMERS_OFFLINE=1
HF_HUB_DISABLE_TELEMETRY=1
HF_HUB_DISABLE_IMPLICIT_TOKEN=1
```

These settings constrain the model clients; they are not a network audit or an assertion about the surrounding agent service.

## Qwen transcription

Extract a mono 16 kHz PCM analysis WAV. Preserve a separate full-quality audio master for rendering. Convert int16 samples using `/ 32768.0`; for another PCM representation, use its actual dtype scale.

Use one gain for the entire analysis recording:

```python
peak = float(np.max(np.abs(audio)))
gain = min(10 ** (12 / 20), 0.95 / peak) if peak > 0 else 1.0
audio = audio.astype(np.float32) * gain
```

Do not normalize every tiny crop separately. A quiet crop must not become noise at speech volume, and blindly multiplying by four can clip.

Starting window recipe: pad speech ranges 300 ms; merge gaps up to 1.2 s; cap windows at 30 s; split long groups near low RMS between 24 and 29 s; overlap adjacent windows by 0.7 s. Record overlaps without deleting their text. These are tunable starting values, not an assumed property of every speaker.

The tested API, after loading the exact local snapshot:

```python
from pathlib import Path
from mlx_audio.stt import load
model = load(Path(local_snapshot))
prediction = model.generate(
    audio_crop_float32,  # mono 16 kHz, at most 30 s in this workflow
    language="Thai", temperature=0.0, max_tokens=2048,
    chunk_duration=60.0, repetition_penalty=None, hotwords=None,
)
text = prediction.text
```

Save each crop's absolute source start/end, overlap, raw text, model revision, settings, and elapsed inference time. These start/end values locate the input, not individual words. If a generation reaches the token cap, mark it truncated and re-crop rather than treating missing text as silence.

Default to no hotwords for deletion decisions. In the tested recording, vocabulary hints improved some names but also echoed the entire vocabulary over non-speech. Unprompted Qwen also produced a word over a long silent interval. Use VAD and waveform as separate evidence.

## Independent Whisper review

Use short crops including preceding/following context. The controlled mlx-whisper setup used `language="th"`, `temperature=0.0`, `condition_on_previous_text=False`, `word_timestamps=True`, and `hallucination_silence_threshold=None`. Treat word times as estimates that still need boundary checks.

A tested `hallucination_silence_threshold=1.5` setting discarded real Thai speech because short subwords were interpreted as anomalies. Disabling it recovered the speech but did not eliminate hallucinations during silence. Therefore, keep VAD and independently inspect suspicious gaps.

The optional Thonburian model is a second opinion, not a guaranteed upgrade for cutting. Its documented fine-tuning does not supply timestamps. Use at most 30 s overlapping crops. It omitted real restarts in one crop and recovered them after shifting the context; it also generated a long hallucination on silence until the token cap. Do not run every model on every minute when only a few seams are uncertain.

No human reference transcript or WER was measured in the original comparison. Do not turn those trial observations into global rankings or accuracy percentages.

## Typhoon Thai CTC alignment

Read the pinned CTC repository's model card and `standalone_align.py` before adapting its head. Use its **matching encoder** rather than assuming any Whisper large-v3 checkpoint is interchangeable. The official Qwen forced-aligner language list in the tested baseline excluded Thai; do not assume it solves Thai timing.

For the tested alternative:

1. Load the audited CTC head architecture and matching encoder with safetensors. Infer on at most 30 s of the same source waveform.
2. Use the feature extractor attention mask to identify valid mel frames; trim padded encoder emissions. The CTC grid is 20 ms.
3. Save log probabilities and vocabulary next to the crop metadata. Re-align changed targets from this cache without reloading the GPU model.
4. Align verified Thai target characters using CTC Viterbi. A NumPy dynamic program avoided a torchaudio dependency in the tested environment. Check blank transitions, repeated consecutive labels, path feasibility, and the target/token mapping; compare tiny cases against exhaustive paths before trusting a new implementation.
5. Reject unsupported target characters explicitly. This vocabulary supports Thai/digits but not Latin product names. Use a documented phonetic mapping when appropriate; never silently remove Latin text and mislabel offsets.
6. Convert crop-relative emissions to source seconds, then inspect the waveform around the proposed cut.

A posterior character spike is not a complete syllable boundary. A 20 ms grid is not 20 ms measured accuracy. Forced paths and raw posterior scores are not calibrated confidence. Agreement between transcripts, CTC evidence, and a safe waveform valley supports a cut; disagreement calls for more context or retaining the speech.

The original implementation passed exhaustive Viterbi checks on four tiny cases and finite-emission/monotonicity checks across 14 real windows. This validates that implementation's mechanics, not a future rewritten aligner or unattended editing accuracy.

## Optional generated inserts — observed 2026-09-13

Use a generative-video model only when the current brief needs it. For designed text, drawn accents or a camera move on an illustration, an existing deterministic Hyperframes/GSAP composition can be the simpler appropriate tool. Do not install several animation libraries or rerun heavy inference merely because the user listed alternatives. Use the available image-generation/editing workflow for requested raster artwork; copy its selected output into the owning project and retain the actual prompt, inputs and tool record there.

Check installed executable identity, supported input mode, cached model components and a real usable output separately. Names such as H3, MiniMax or Wan in a request do not prove a particular CLI/API exists, accepts reference video, or is running locally. Inspect the actual runtime's help/model-header inspection before choosing text-to-video, first-frame conditioning or reference-video mode. A missing external source drive is not evidence that a model was never installed. Verify mounts and source paths first, then resume the retained job state without duplicate downloads or generations.

One successful local MiniMax-H3 example used `~/Documents/ChatGPT/minimax-h3/runtimes/h3.c/h3` at revision `8974cc0` with verified cached FL2VA components and `--first-frame`. Native output was 1024×576, 141 frames at 24 fps; generation took 1,240.76 seconds on the tested M5 Max/48 GiB machine. It was normalized to 176 silent frames at 1080p30 and fully decoded. Those are observed run values, not a speed promise, memory minimum, arbitrary frame-count rule or proof of another input mode. Native resolution/rate and normalized delivery resolution/rate must be recorded separately.

Coordinate heavy model jobs so agents do not load duplicate models into shared memory. Prepare captions, source mapping and lightweight graphic work while one verified generation runs. Report job state from its actual process/log; an installed binary, prompt file or poster preview is not generated video. Inspect the finished motion, text and recognizable symbols before using it. If the user rejects the conditioning image or asks for a new original visual, replace the derived take too; do not retain it to justify spent render time.

The local H3 shot above passed technical and visual checks but was later excluded by the user's artwork change. The delivered alternative used a newly generated unbranded AI illustration with deterministic motion. Safe procedure/provenance pointers: `/Volumes/BoomBigNose/EP211/work/full-edit-v4/astra-h3/README.md`, `provenance.json` beside it, and `../ai-original/provenance.json`. Media, prompts and private speech stay in the episode; historical records do not authorize a new cloud call or publication.
