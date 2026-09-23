# Catalog schema v1

The source of truth is `data/*.yaml`. `README.md` and `dist/index.json` are **generated**
from it by `scripts/build.py` — never edit them by hand.

---

## Why YAML instead of a markdown table

An "awesome-list" style table never becomes more than a pile of links. Steps 2–4 of this
project (comparison site, block composition, local export) all assume a **machine-readable
catalog**.

Step 3 in particular only works if every model declares **what it accepts and what it
produces**, so the editor can decide whether two blocks may be connected. Adding that field
later would mean revisiting every entry, so it is required from the start.

---

## Record shape

```yaml
- id: qwen3-embedding-8b          # globally unique, lowercase + hyphens
  name: Qwen3-Embedding-8B
  category: embedding             # see the category table below
  task: text-embedding            # finer-grained task
  vendor: Alibaba
  repo_id: Qwen/Qwen3-Embedding-8B  # exact Hugging Face repo, for scripts/fetch.py

  # ── Composability (the basis for step 3) ──
  inputs:  [text]
  outputs: [embedding]

  # ── Licensing (where people most often get burned) ──
  license: Apache-2.0
  openness: open-weight           # open-source | open-weight
  commercial_use: yes             # yes | no | conditional
  license_note: null

  # ── Runtime requirements ──
  params: 8B                      # free text, for display
  params_b: 8                     # TOTAL parameters in billions, numeric
  params_note: null               # e.g. MoE caveats
  vram_min_gb: 16                 # stated figure only; null if unverified
  runs_on: [gpu]                  # cpu | gpu | edge | apple-silicon

  # ── What it is actually good at (the basis for choosing) ──
  specialization: >
    Supports 100+ natural and programming languages. Accepts user-defined instructions,
    so behaviour can be tuned per domain.
  strengths: [multilingual, instruction-tunable]
  weaknesses: [gpu-required]

  # ── Links and provenance ──
  links:
    huggingface: https://huggingface.co/Qwen/Qwen3-Embedding-8B
    github: null
    paper: https://arxiv.org/abs/2506.05176
  released: 2025-06
  benchmarks:
    - name: MTEB
      value: leading
      note: as of the 2026-09 snapshot
  sources:
    - https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models
  verified: 2026-09-23
```

---

## Required fields

| Field | Required | Notes |
|---|---|---|
| `id` | ✔ | Globally unique identifier |
| `name` | ✔ | Display name |
| `category` | ✔ | See category table |
| `inputs` / `outputs` | ✔ | **Type lists. The basis for connection checks** |
| `license` | ✔ (key) | SPDX identifier or license name. **May be `null` if unverified** |
| `openness` | ✔ | `open-source` (OSI-approved) or `open-weight` |
| `commercial_use` | ✔ | `yes` / `no` / `conditional` |
| `specialization` | ✔ | One paragraph: what is this good at |
| `sources` | ✔ | URLs backing the information |

**Leave unknown values as `null`.** Do not guess — a wrong VRAM figure or license costs the
reader real time and money. The validator reports these as warnings, not errors.

> **YAML gotcha:** bare `yes` / `no` parse as booleans under YAML 1.1. The loader normalizes
> them back to strings, so you may write either form.

---

## Categories

| Category | Description |
|---|---|
| `llm` | Large language models (text generation and reasoning) |
| `slm` | Small language models (on-device, edge) |
| `vlm` | Vision-language models (image understanding) |
| `vision` | Classical computer vision (detection, segmentation, OCR) |
| `asr` | Speech recognition |
| `tts` | Text to speech |
| `image-gen` | Image generation |
| `video-gen` | Video generation |
| `embedding` | Embedding and reranking |
| `agent` | Agent-specialized models and frameworks |

## Input and output types

The block editor allows a connection **only when an output type of one model appears in the
inputs of the next**.

| Type | Description |
|---|---|
| `text` | Natural-language text |
| `image` | Still image |
| `video` | Video |
| `audio` | General audio |
| `speech` | Speech (ASR input / TTS output) |
| `boxes` | Bounding boxes |
| `mask` | Segmentation mask |
| `embedding` | Vector |
| `score` | Scores or rankings (reranker output) |

### Worked example

*Feed an image, get a spoken description* — validated by types alone:

```
[image] → VLM (inputs:[image,text] outputs:[text])
        → TTS (inputs:[text] outputs:[speech]) → [speech]
```

```
[image] → detector (outputs:[boxes]) → LLM (inputs:[text])  ✕  type mismatch
[image] → VLM      (outputs:[text])  → LLM (inputs:[text])  ○
```

---

## Why licensing is a first-class field

This is where mistakes are most expensive. **XTTS-v2 is the most-downloaded TTS model on
Hugging Face, yet its weights fall under the Coqui Public Model License — non-commercial use
only.** Ship it without checking and the whole thing has to come back out later.

Separately, most widely used models (Llama, Qwen, Gemma, DeepSeek, Kimi, GLM) are **not
OSI open-source — they are open-weight.** The `openness` field records that distinction, and
`commercial_use` records the practical consequence.

---

## Downloading weights

This repository **does not host model weights** and never will. Three reasons:

1. **Licensing.** Redistributing weights is a separate permission from using them.
   Several models here — XTTS-v2 among them — forbid it outright, and others
   (Llama, Gemma) attach conditions to any redistribution.
2. **Size.** The 14 entries with a known parameter count total roughly **9.5 TB** at
   fp16. Kimi K3 alone is about 5.6 TB.
3. **Platform limits.** GitHub blocks files over 100 MiB, and Git LFS on Free/Pro
   includes 10 GiB of storage and bandwidth.

Instead, `scripts/fetch.py` pulls from the original publisher into a local, gitignored
`models/` directory, showing the license terms first:

```bash
python3 scripts/fetch.py --list       # what has a repo recorded
python3 scripts/fetch.py kokoro       # fetch one
python3 scripts/fetch.py --status     # what is already local
```

`repo_id` is what makes a model fetchable. A `links.huggingface` value pointing at an
organization page is not enough — record the exact repo. **Verify a repo id resolves
before adding it**; a wrong path produces a 404 at download time, not at review time.

`models/manifest.json` records the exact revision of everything fetched and **is**
committed, so a working setup can be reproduced without shipping the weights.

## VRAM requirements

Two fields feed the hardware check in `scripts/check_env.py`:

- **`vram_min_gb`** — a figure stated by the vendor or a benchmark. Leave `null` if you
  have not seen one; do not derive it yourself.
- **`params_b`** — total parameters in billions, as a number. The checker estimates VRAM
  from this when no stated figure exists.

The estimate is:

```
vram_gb = params_b × bytes_per_param × 1.2
          fp16 2.0 · int8 1.0 · int4 0.55
```

The 1.2 covers activations and a modest KV cache. Estimated figures are always printed
with a `~` prefix so they are never mistaken for measured requirements.

> **Mixture-of-experts:** `params_b` is the **total**, not the active, parameter count.
> Every expert must be resident in memory to be routed to, so a 552B/8B-active model needs
> VRAM for 552B. Record the active count in `params_note`.

Checking your own machine:

```bash
python3 scripts/check_env.py               # what runs here
python3 scripts/check_env.py --all         # include models that do not fit
python3 scripts/check_env.py --precision int8
python3 scripts/check_env.py --json        # machine-readable
```

## Validation

```bash
python3 scripts/validate.py      # schema, types, duplicate ids
python3 scripts/build.py         # regenerate README.md and dist/index.json
```
