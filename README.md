# ModelAtlas

> A catalog of open-source and open-weight AI models — **find them by what they do, check the license, and compose them into pipelines.**

**41 models · 9 categories** · last updated 2026-09-23

| | |
|---|---|
| Free for commercial use | 25 |
| Conditional or prohibited | 16 |
| License unverified | 9 |

---

## What makes this different

**1. Structured data, not a link list.**  
The source of truth is [`data/*.yaml`](data/). This README and [`dist/index.json`](dist/index.json) are generated from it.

**2. Every model declares its input and output types.**  
That is what lets a machine decide *which model can follow which*. See [Composing models](#composing-models) below.

**3. Licensing is a first-class field.**  
This is where people get burned. **XTTS-v2 is the most-downloaded TTS model on Hugging Face, yet its weights are non-commercial only.** And most widely used models (Llama, Qwen, Gemma, DeepSeek, Kimi, GLM) are **open-weight, not OSI open-source** — the `openness` field records that distinction.

**4. Unknown values are left empty.**  
Guessing a VRAM requirement or a license costs the reader real money. Unverified fields show as `—` and the validator flags them.

---

## Categories

- [Large Language Models (7)](#llm)
- [Small Language Models (1)](#slm)
- [Vision-Language Models (4)](#vlm)
- [Computer Vision (6)](#vision)
- [Speech Recognition (5)](#asr)
- [Text to Speech (5)](#tts)
- [Image Generation (4)](#image-gen)
- [Video Generation (5)](#video-gen)
- [Embedding & Reranking (4)](#embedding)

---

<a id="llm"></a>

## Large Language Models

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **DeepSeek-V4.1-Flash** | MoE design keeps active parameters small, so inference is cheap for its size. MIT licensed, so commercial us… | `text` → `text` | MIT <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/deepseek-ai) · [GH](https://github.com/deepseek-ai) |
| **GLM-5.3** | Frontier-class open-weight model, near the top on aggregate benchmarks. | `text` → `text` | GLM License <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/zai-org) |
| **GLM-5.3-Flash** | The most permissively licensed model in the GLM-5.3 family. 18B active parameters keep inference cost low. | `text` → `text` | MIT <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/zai-org) |
| **Kimi K3** | Strong on agentic and terminal work. Among the top open-weight models as of its July 2026 release. | `text` → `text` | Modified MIT <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/moonshotai) |
| **Qwen3.6-27B** | A dense 27B that fits on one GPU yet approaches frontier-class coding scores. Best performance-per-host in t… | `text` → `text` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Qwen3.8 Max** | Ranked first on the September 2026 open-weight leaderboard. | `text` → `text` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Qwen3.8-27B** | Runs on a single 24GB GPU or a 32GB Mac. The safest default when local execution is a requirement. | `text` → `text` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu, apple-silicon · 24GB+ | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |

<a id="slm"></a>

## Small Language Models

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **Gemma 4** | Among the strongest small models that fit under 16GB. The default pick for laptops and low-end GPUs when eve… | `text` → `text` | Gemma Terms of Use <sup>weights</sup> | ⚠️ Conditional | gpu, cpu, apple-silicon · 16GB+ | [HF](https://huggingface.co/google) |

<a id="vlm"></a>

## Vision-Language Models

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **GLM-4.5V** | Strong 3D reasoning. Reported state of the art among similarly sized open models across 42 public benchmarks. | `image,text` → `text` | — <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/zai-org) |
| **InternVL3.5** | A visual-resolution router improves inference efficiency. The 241B flagship is state of the art among open V… | `image,text` → `text` | — <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/OpenGVLab) · [GH](https://github.com/OpenGVLab/InternVL) |
| **Qwen2.5-VL-32B-Instruct** | Particularly well suited to visual agents — driving a UI, navigating documents, and other tasks where the mo… | `image,text` → `text` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Qwen3-VL** | Front of the pack on both quality and latency among 2026 open VLMs. Used for image description, document und… | `image,text` → `text` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |

<a id="vision"></a>

## Computer Vision

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **Florence-2** | Handles OCR and vision-language tasks in one model. Captioning, detection and OCR are switched by prompt, wh… | `image,text` → `text,boxes` | MIT <sup>OSI</sup> | ✅ Yes | gpu, cpu | [HF](https://huggingface.co/microsoft/Florence-2-large) |
| **GLM-OCR** | Extracts text from document images. Among the leading OCR options as of 2026. | `image` → `text` | — <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/zai-org) |
| **RF-DETR** | Tops both COCO and the real-world RF100-VL benchmark. The recommended accuracy-first starting point for most… | `image` → `boxes,mask` | Apache-2.0 <sup>OSI</sup> | ✅ Yes | gpu | [GH](https://github.com/roboflow/rf-detr) |
| **SAM 2** | Carries memory across video frames, so an object picked by click, box or mask is tracked to the end of the c… | `image,video` → `mask` | Apache-2.0 <sup>OSI</sup> | ✅ Yes | gpu | [GH](https://github.com/facebookresearch/sam2) |
| **SAM 3** | Supports both promptable and open-vocabulary segmentation. Especially useful for building labelled datasets … | `image,video,text` → `mask` | — <sup>weights</sup> | ⚠️ Conditional | gpu | [GH](https://github.com/facebookresearch) |
| **YOLO26** | Optimized for edge and real-time use. NMS-free end-to-end prediction simplifies post-processing, and CPU inf… | `image,video` → `boxes,mask` | AGPL-3.0 <sup>OSI</sup> | ⚠️ Conditional | gpu, cpu, edge | [GH](https://github.com/ultralytics/ultralytics) · [paper](https://arxiv.org/abs/2606.03748) |

<a id="asr"></a>

## Speech Recognition

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **Moonshine** | Built for real-time recognition on constrained hardware. At 27MB the smallest model fits where Whisper and t… | `speech` → `text` | MIT <sup>OSI</sup> | ✅ Yes | cpu, edge | [GH](https://github.com/usefulsensors/moonshine) |
| **NVIDIA Canary-Qwen 2.5B** | Currently the most accurate option for English. Beats Whisper on English-only workloads. | `speech` → `text` | — <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/nvidia) |
| **NVIDIA Parakeet TDT** | The fastest self-hostable option for batch throughput. Pick it when transcribing a large archive in one pass. | `speech` → `text` | — <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/nvidia) |
| **Qwen3-ASR** | Covers 52 languages and dialects, handling language identification, recognition and timestamp prediction in … | `speech` → `text` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Whisper large-v3** | Still the safest all-rounder for general transcription. Broad language coverage makes it the default when th… | `speech` → `text` | MIT <sup>OSI</sup> | ✅ Yes | gpu, cpu | [HF](https://huggingface.co/openai/whisper-large-v3) · [GH](https://github.com/openai/whisper) |

<a id="tts"></a>

## Text to Speech

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **Chatterbox** | Safe for commercial deployment and still supports voice cloning — the usual license-safe alternative to XTTS… | `text,speech` → `speech` | MIT <sup>OSI</sup> | ✅ Yes | gpu | [GH](https://github.com/resemble-ai/chatterbox) |
| **F5-TTS** | Flow-matching based, with notably good voice cloning — give it a reference clip and it synthesizes in that v… | `text,speech` → `speech` | MIT <sup>OSI</sup> | ✅ Yes | gpu | [GH](https://github.com/SWivid/F5-TTS) · [paper](https://arxiv.org/abs/2410.06885) |
| **Kokoro** | Very light at 82M parameters, fast enough on CPU to be the easiest final stage in a local pipeline. It canno… | `text` → `speech` | Apache-2.0 <sup>OSI</sup> | ✅ Yes | cpu, gpu, edge | [HF](https://huggingface.co/hexgrad/Kokoro-82M) |
| **Qwen3-TTS** | One of the safe picks for commercial deployment, and easy to pair with other models in the Qwen ecosystem. | `text` → `speech` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **XTTS-v2** | Clones a voice into another language from a six-second sample. Capable, but the license rules out commercial… | `text,speech` → `speech` | Coqui Public Model License <sup>weights</sup> | ❌ No | gpu | [HF](https://huggingface.co/coqui/XTTS-v2) |

<a id="image-gen"></a>

## Image Generation

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **FLUX.2** | Leads open models on photorealism and output quality. Pick it when the result has to stand up as professiona… | `text,image` → `image` | — <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/black-forest-labs) |
| **Qwen-Image** | An image model that is unrestricted for commercial use, and reported to render text inside images unusually … | `text,image` → `image` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Stable Diffusion 3.5** | Deepest ecosystem and the most flexible for fine-tuning. LoRA, ControlNet and the rest of the tooling are ri… | `text,image` → `image` | Stability Community License <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/stabilityai) |
| **Z-Image Turbo** | Matches or beats FLUX.2 [dev], HunyuanImage 3.0 and Imagen 4 while needing only a few inference steps. Usefu… | `text` → `image` | — <sup>weights</sup> | ⚠️ Conditional | gpu | — |

<a id="video-gen"></a>

## Video Generation

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **CogVideoX** | Released early enough to have accumulated tooling and examples — helpful when fine-tuning references are nee… | `text,image` → `video` | Apache-2.0 <sup>OSI</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/zai-org) · [GH](https://github.com/zai-org/CogVideo) |
| **HunyuanVideo 1.5** | Runs on a single RTX 4090 at roughly 14GB of VRAM with FP8 and CPU offloading. A candidate when one consumer… | `text,image` → `video` | Tencent Hunyuan Community License <sup>weights</sup> | ⚠️ Conditional | gpu · 14GB+ | [HF](https://huggingface.co/tencent) · [GH](https://github.com/Tencent-Hunyuan) |
| **LTX-2.3** | The only open model with native audio: it generates synchronized sound and video in a single diffusion pass,… | `text,image` → `video,audio` | — <sup>weights</sup> | ⚠️ Conditional | gpu | [HF](https://huggingface.co/Lightricks) · [GH](https://github.com/Lightricks/LTX-Video) |
| **Mochi 1** | An Apache-2.0 video model, reported to be strong on motion. | `text` → `video` | Apache-2.0 <sup>OSI</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/genmo) · [GH](https://github.com/genmoai/mochi) |
| **Wan 2.2** | Apache-2.0, so commercial use is unrestricted, and the 5B GGUF runs in 8GB of VRAM with memory offloading. T… | `text,image` → `video` | Apache-2.0 <sup>OSI</sup> | ✅ Yes | gpu · 8GB+ | [HF](https://huggingface.co/Wan-AI) · [GH](https://github.com/Wan-Video) |

<a id="embedding"></a>

## Embedding & Reranking

| Model | Best at | In → Out | License | Commercial | Runs on | Links |
|---|---|---|---|---|---|---|
| **BGE-M3** | The self-hosted multilingual standard across 100+ languages. The default alternative to Qwen3 where a larger… | `text` → `embedding` | MIT <sup>OSI</sup> | ✅ Yes | gpu, cpu | [HF](https://huggingface.co/BAAI/bge-m3) · [GH](https://github.com/FlagOpen/FlagEmbedding) |
| **BGE-reranker-v2** | Reranks embedding search results. Paired with BGE-M3 it completes a two-stage retrieval pipeline at zero lic… | `text` → `score` | Apache-2.0 <sup>OSI</sup> | ✅ Yes | gpu, cpu | [HF](https://huggingface.co/BAAI) · [GH](https://github.com/FlagOpen/FlagEmbedding) |
| **Qwen3-Embedding-8B** | Covers 100+ natural and programming languages and leads the MTEB snapshot. Accepts user-defined instructions… | `text` → `embedding` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) · [paper](https://arxiv.org/abs/2506.05176) |
| **Qwen3-VL-Embedding** | Places text and images in one vector space, so you can retrieve documents by image or images by text. A matc… | `text,image` → `embedding` | Apache-2.0 <sup>weights</sup> | ✅ Yes | gpu | [HF](https://huggingface.co/Qwen) · [paper](https://arxiv.org/abs/2601.04720) |

---

<a id="composing-models"></a>

## Composing models

Each model declares `inputs` and `outputs`. Two models connect only when an output type of the first appears in the inputs of the second.

**Types**  `text` · `image` · `video` · `audio` · `speech` · `boxes` · `mask` · `embedding` · `score`

### Example — describe an image and read it aloud

```
[image] ──▶ Qwen3-VL          ──▶ Kokoro        ──▶ [speech]
            inputs:  image,text     inputs:  text
            outputs: text           outputs: speech
```

Both are free for commercial use, and Kokoro is 82M parameters so it runs on CPU.

### Example — answer a spoken question with speech

```
[speech] ─▶ Whisper large-v3 ─▶ Qwen3.8-27B ─▶ Kokoro ─▶ [speech]
            speech→text          text→text       text→speech
```

### When types do not line up

```
[image] ─▶ YOLO26 (→boxes)    ─▶ Qwen3.8-27B (text→)  ✕  cannot accept boxes
[image] ─▶ Florence-2 (→text) ─▶ Qwen3.8-27B (text→)  ○
```

### Category connection matrix

Generated from the type declarations. Each cell counts the connectable model pairs.

| from \ to | Large Language Models | Small Language Models | Vision-Language Models | Computer Vision | Speech Recognition | Text to Speech | Image Generation | Video Generation | Embedding & Reranking |
|---|---|---|---|---|---|---|---|---|---|
| Large Language Models | 42 | 7 | 28 | 14 | · | 35 | 28 | 35 | 28 |
| Small Language Models | 7 | · | 4 | 2 | · | 5 | 4 | 5 | 4 |
| Vision-Language Models | 28 | 4 | 12 | 8 | · | 20 | 16 | 20 | 16 |
| Computer Vision | 14 | 2 | 8 | 3 | · | 10 | 8 | 10 | 8 |
| Speech Recognition | 35 | 5 | 20 | 10 | · | 25 | 20 | 25 | 20 |
| Text to Speech | · | · | · | · | 25 | 12 | · | · | · |
| Image Generation | · | · | 16 | 24 | · | · | 9 | 16 | 4 |
| Video Generation | · | · | · | 15 | · | · | · | · | · |
| Embedding & Reranking | · | · | · | · | · | · | · | · | · |

---

## Contributing

Add a model by appending an entry to the matching YAML file in [`data/`](data/), then run:

```bash
python3 scripts/validate.py   # schema, types, duplicate ids
python3 scripts/build.py      # regenerate README.md and dist/index.json
```

Field definitions are in [SCHEMA.md](SCHEMA.md). **Leave unknown values as `null` — do not guess.** See [CONTRIBUTING.md](CONTRIBUTING.md).

## Roadmap

- [x] **Step 1** — structured model catalog *(you are here)*
- [ ] **Step 2** — comparison site with side-by-side inference on the same input
- [ ] **Step 3** — block/graph editor to compose models into a product
- [ ] **Step 4** — export a composed pipeline that runs locally

## License

Catalog data and documentation: **CC BY 4.0**. Code under `scripts/`: **MIT**. See [LICENSE](LICENSE).

Each listed model carries its own license — always check the model's own terms before use. The `license` field here is a pointer, not legal advice.

---

<sub>This catalog is curated, not exhaustive. Hugging Face alone hosts millions of repositories; a complete list would not help anyone choose. Every entry carries a `sources` field pointing at where its information came from.</sub>
