# ModelAtlas

> 공개된 오픈소스·오픈웨이트 AI 모델을 **용도별로 찾고, 라이선스를 확인하고, 조합해서 쓰기** 위한 카탈로그.

**모델 41개 · 카테고리 9개** · 최종 갱신 2026-09-23

| | |
|---|---|
| 상업 사용 자유 | 25개 |
| 조건부·불가 | 16개 |
| 라이선스 미확인 | 9개 |

---

## 이 카탈로그가 다른 점

**1. 링크 모음이 아니라 구조화된 데이터입니다.**  
원본은 [`data/*.yaml`](data/)이고 이 README 와 [`dist/index.json`](dist/index.json)은 거기서 생성됩니다.

**2. 모델마다 입출력 타입이 선언되어 있습니다.**  
그래서 *어떤 모델을 어떤 모델 뒤에 붙일 수 있는지* 기계가 판정합니다. 아래 조합 예시 참조.

**3. 라이선스를 1급 정보로 다룹니다.**  
가장 흔한 사고가 여기서 납니다. 예를 들어 **XTTS-v2 는 HuggingFace 최다 다운로드 TTS 모델이지만 비상업 용도만 허용**합니다. 
또한 널리 쓰이는 모델 대부분(Llama·Qwen·Gemma·DeepSeek·Kimi·GLM)은 OSI 기준 오픈소스가 아니라 **오픈웨이트**입니다.

**4. 모르는 값은 비워 둡니다.**  
VRAM 요건이나 라이선스를 추측해서 적으면 사용자가 실제로 손해를 봅니다. 미확인은 `—` 로 표시됩니다.

---

## 카테고리

- [대형 언어 모델 (7)](#llm)
- [소형 언어 모델 (1)](#slm)
- [비전-언어 모델 (4)](#vlm)
- [컴퓨터 비전 (6)](#vision)
- [음성 인식 (5)](#asr)
- [음성 합성 (5)](#tts)
- [이미지 생성 (4)](#image-gen)
- [영상 생성 (5)](#video-gen)
- [임베딩·리랭킹 (4)](#embedding)

---

<a id="llm"></a>

## 대형 언어 모델

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **DeepSeek-V4.1-Flash** | MoE 구조로 활성 파라미터가 매우 작아 추론 비용이 낮다. MIT 라이선스로 상업 사용이 자유롭다. | `text` → `text` | MIT <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/deepseek-ai) · [GH](https://github.com/deepseek-ai) |
| **GLM-5.3** | 프런티어급 오픈 웨이트 모델. 종합 성능 상위권. | `text` → `text` | GLM License <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/zai-org) |
| **GLM-5.3-Flash** | GLM-5.3 계열 중 라이선스가 가장 자유롭다. 활성 파라미터 18B로 추론 부담이 낮다. | `text` → `text` | MIT <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/zai-org) |
| **Kimi K3** | 에이전트·터미널 작업에 강하다. 2026년 7월 공개 시점 기준 오픈 웨이트 최상위권. | `text` → `text` | Modified MIT <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/moonshotai) |
| **Qwen3.6-27B** | 단일 GPU에서 돌아가는 dense 27B인데 코딩 벤치마크가 프런티어급에 근접한다. 자체 호스팅 대비 성능비가 가장 좋은 구간. | `text` → `text` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Qwen3.8 Max** | 2026년 9월 오픈 웨이트 종합 순위 1위. | `text` → `text` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Qwen3.8-27B** | 24GB 단일 GPU 또는 32GB 맥에서 실행 가능. 로컬 실행을 전제할 때 가장 무난한 선택. | `text` → `text` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu, apple-silicon · 24GB+ | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |

<a id="slm"></a>

## 소형 언어 모델

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **Gemma 4** | 16GB 미만 환경에서 쓸 수 있는 소형 모델 중 성능이 가장 나은 축. 노트북·저사양 GPU에서 로컬 실행을 전제할 때의 기본 선택지. | `text` → `text` | Gemma Terms of Use <sup>가중치</sup> | ⚠️ 조건부 | gpu, cpu, apple-silicon · 16GB+ | [HF](https://huggingface.co/google) |

<a id="vlm"></a>

## 비전-언어 모델

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **GLM-4.5V** | 3D 추론이 강점. 공개 벤치마크 42종에서 동급 오픈소스 모델 중 최상위를 기록했다. | `image,text` → `text` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/zai-org) |
| **InternVL3.5** | 시각 해상도 라우터로 추론 효율을 높였다. 플래그십 241B 는 오픈소스 VLM 중 SOTA. | `image,text` → `text` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/OpenGVLab) · [GH](https://github.com/OpenGVLab/InternVL) |
| **Qwen2.5-VL-32B-Instruct** | 시각 에이전트 용도에 특히 잘 맞는다. UI 조작·문서 탐색처럼 이미지를 보고 행동을 결정하는 작업에 쓰인다. | `image,text` → `text` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Qwen3-VL** | 2026년 오픈소스 VLM 중 성능·지연 양쪽에서 선두권. 이미지 설명·문서 이해· 시각 에이전트에 두루 쓰인다. 조합 파이프라인의 표준 출발점. | `image,text` → `text` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |

<a id="vision"></a>

## 컴퓨터 비전

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **Florence-2** | OCR 과 비전-언어 작업을 한 모델로 처리한다. 캡셔닝·검출·OCR 을 프롬프트로 전환하며 쓸 수 있어 조합 파이프라인에 넣기 편하다. | `image,text` → `text,boxes` | MIT <sup>OSI</sup> | ✅ 가능 | gpu, cpu | [HF](https://huggingface.co/microsoft/Florence-2-large) |
| **GLM-OCR** | 문서 이미지에서 텍스트를 추출한다. 2026년 기준 OCR 용도 선두권. | `image` → `text` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/zai-org) |
| **RF-DETR** | COCO 와 실환경 벤치마크(RF100-VL) 양쪽에서 1위. 대부분의 비전 프로젝트에서 정확도 기준 첫 선택지로 권장된다. | `image` → `boxes,mask` | Apache-2.0 <sup>OSI</sup> | ✅ 가능 | gpu | [GH](https://github.com/roboflow/rf-detr) |
| **SAM 2** | 영상에서 프레임 간 메모리를 유지해 클릭·박스·마스크로 선택한 객체를 끝까지 추적한다. 영상 분할이 필요하면 여기부터 본다. | `image,video` → `mask` | Apache-2.0 <sup>OSI</sup> | ✅ 가능 | gpu | [GH](https://github.com/facebookresearch/sam2) |
| **SAM 3** | 프롬프트 기반 분할과 open-vocabulary 분할을 함께 지원한다. 데이터셋 라벨링을 빠르게 만들 때 특히 유용하다. | `image,video,text` → `mask` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | [GH](https://github.com/facebookresearch) |
| **YOLO26** | 엣지·실시간에 최적화. NMS 없는 end-to-end 예측으로 후처리가 단순하고, CPU 추론이 YOLO11-N 대비 최대 43% 빠르다. 검출·분할·분류·… | `image,video` → `boxes,mask` | AGPL-3.0 <sup>OSI</sup> | ⚠️ 조건부 | gpu, cpu, edge | [GH](https://github.com/ultralytics/ultralytics) · [논문](https://arxiv.org/abs/2606.03748) |

<a id="asr"></a>

## 음성 인식

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **Moonshine** | 저사양 하드웨어의 실시간 인식을 목표로 만들어졌다. 최소 모델이 27MB 라 Whisper 나 NVIDIA 모델이 아예 못 도는 환경에 들어간다. | `speech` → `text` | MIT <sup>OSI</sup> | ✅ 가능 | cpu, edge · CPU | [GH](https://github.com/usefulsensors/moonshine) |
| **NVIDIA Canary-Qwen 2.5B** | 영어 정확도 기준 현재 최상위. 영어 전용 워크로드라면 Whisper 보다 낫다. | `speech` → `text` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/nvidia) |
| **NVIDIA Parakeet TDT** | 자체 호스팅 가능한 것 중 배치 처리량이 가장 빠르다. 대량 아카이브를 한 번에 전사할 때 선택. | `speech` → `text` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/nvidia) |
| **Qwen3-ASR** | 52개 언어·방언 지원. 언어 식별, 음성 인식, 타임스탬프 예측을 한 모델로 처리한다. 자막 생성처럼 타임스탬프가 필요한 파이프라인에 적합. | `speech` → `text` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Whisper large-v3** | 범용 전사에서 여전히 가장 무난한 올라운더. 언어 커버리지가 넓어 입력 언어를 특정할 수 없을 때 기본값으로 쓴다. | `speech` → `text` | MIT <sup>OSI</sup> | ✅ 가능 | gpu, cpu | [HF](https://huggingface.co/openai/whisper-large-v3) · [GH](https://github.com/openai/whisper) |

<a id="tts"></a>

## 음성 합성

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **Chatterbox** | 상업 배포가 안전하면서 음성 복제를 지원한다. XTTS-v2 의 라이선스 대안으로 자주 거론된다. | `text,speech` → `speech` | MIT <sup>OSI</sup> | ✅ 가능 | gpu | [GH](https://github.com/resemble-ai/chatterbox) |
| **F5-TTS** | flow matching 기반. 음성 복제 품질이 특히 좋아 참조 음성을 주면 해당 목소리로 합성한다. 품질 우선이면 여기부터. | `text,speech` → `speech` | MIT <sup>OSI</sup> | ✅ 가능 | gpu | [GH](https://github.com/SWivid/F5-TTS) · [논문](https://arxiv.org/abs/2410.06885) |
| **Kokoro** | 82M 파라미터로 매우 가볍다. CPU 에서도 실용적인 속도가 나와 로컬 조합 파이프라인의 마지막 단계로 넣기 가장 쉽다. 다만 음성 샘플로 목소리를 복제하는… | `text` → `speech` | Apache-2.0 <sup>OSI</sup> | ✅ 가능 | cpu, gpu, edge · CPU | [HF](https://huggingface.co/hexgrad/Kokoro-82M) |
| **Qwen3-TTS** | 상업 배포가 안전한 선택지 중 하나. Qwen 생태계의 다른 모델과 조합하기 좋다. | `text` → `speech` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **XTTS-v2** | 6초 샘플만으로 다른 언어로 목소리를 복제한다. 기능은 뛰어나지만 라이선스 때문에 상업 사용은 불가하다. | `text,speech` → `speech` | Coqui Public Model License <sup>가중치</sup> | ❌ 불가 | gpu | [HF](https://huggingface.co/coqui/XTTS-v2) |

<a id="image-gen"></a>

## 이미지 생성

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **FLUX.2** | 사실감과 출력 품질에서 오픈 모델 중 선두. 전문 작업물 품질이 필요할 때 선택. | `text,image` → `image` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/black-forest-labs) |
| **Qwen-Image** | 상업 사용이 자유로운 이미지 생성 모델. 텍스트 렌더링 품질이 좋은 편으로 알려져 있다. | `text,image` → `image` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) |
| **Stable Diffusion 3.5** | 생태계 깊이와 파인튜닝 유연성이 최대 강점. LoRA·ControlNet 등 주변 도구가 가장 많아 커스터마이징이 필요하면 여기가 유리하다. | `text,image` → `image` | Stability Community License <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/stabilityai) |
| **Z-Image Turbo** | 추론 스텝이 매우 적은데도 FLUX.2 dev, HunyuanImage 3.0, Imagen 4 급 품질을 낸다. 지연이 중요한 조합 파이프라인에 유리하다. | `text` → `image` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | — |

<a id="video-gen"></a>

## 영상 생성

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **CogVideoX** | 비교적 초기부터 공개되어 주변 도구와 예제가 많다. 파인튜닝 자료가 필요할 때 유리. | `text,image` → `video` | Apache-2.0 <sup>OSI</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/zai-org) · [GH](https://github.com/zai-org/CogVideo) |
| **HunyuanVideo 1.5** | FP8 과 CPU 오프로딩을 쓰면 RTX 4090 단일 GPU, 약 14GB VRAM 에서 실행된다. 소비자용 GPU 한 장으로 돌리는 것이 목표라면 후보. | `text,image` → `video` | Tencent Hunyuan Community License <sup>가중치</sup> | ⚠️ 조건부 | gpu · 14GB+ | [HF](https://huggingface.co/tencent) · [GH](https://github.com/Tencent-Hunyuan) |
| **LTX-2.3** | 오픈 모델 중 유일하게 네이티브 오디오를 지원한다. 영상과 동기화된 소리를 한 번의 디퓨전 패스에서 함께 생성하며 4K·50fps 출력이 가능하다. 후처리로 … | `text,image` → `video,audio` | — <sup>가중치</sup> | ⚠️ 조건부 | gpu | [HF](https://huggingface.co/Lightricks) · [GH](https://github.com/Lightricks/LTX-Video) |
| **Mochi 1** | Apache-2.0 영상 생성 모델. 동작 표현이 강점으로 알려져 있다. | `text` → `video` | Apache-2.0 <sup>OSI</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/genmo) · [GH](https://github.com/genmoai/mochi) |
| **Wan 2.2** | Apache-2.0 로 상업 사용이 자유롭고, 5B GGUF 에 메모리 오프로딩을 쓰면 VRAM 8GB 에서도 돈다. 로컬 실행 전제라면 가장 현실적인 선택.… | `text,image` → `video` | Apache-2.0 <sup>OSI</sup> | ✅ 가능 | gpu · 8GB+ | [HF](https://huggingface.co/Wan-AI) · [GH](https://github.com/Wan-Video) |

<a id="embedding"></a>

## 임베딩·리랭킹

| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |
|---|---|---|---|---|---|---|
| **BGE-M3** | 100개 이상 언어를 다루는 다국어 자체 호스팅 표준. 큰 모델을 띄우기 어려운 환경에서 Qwen3 대신 쓰는 기본 선택지. | `text` → `embedding` | MIT <sup>OSI</sup> | ✅ 가능 | gpu, cpu | [HF](https://huggingface.co/BAAI/bge-m3) · [GH](https://github.com/FlagOpen/FlagEmbedding) |
| **BGE-reranker-v2** | 임베딩 검색 결과를 재정렬한다. BGE-M3 와 묶으면 라이선스 비용 0 으로 2단계 검색 파이프라인이 완성된다. | `text` → `score` | Apache-2.0 <sup>OSI</sup> | ✅ 가능 | gpu, cpu | [HF](https://huggingface.co/BAAI) · [GH](https://github.com/FlagOpen/FlagEmbedding) |
| **Qwen3-Embedding-8B** | 100개 이상의 자연어·프로그래밍 언어를 지원하고 MTEB 선두권. 사용자 정의 지시문을 받아 도메인별로 동작을 조정할 수 있다. 0.6B · 4B 변형이 있… | `text` → `embedding` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [GH](https://github.com/QwenLM) · [논문](https://arxiv.org/abs/2506.05176) |
| **Qwen3-VL-Embedding** | 텍스트와 이미지를 같은 벡터 공간에 넣는다. 이미지로 문서를 찾거나 텍스트로 이미지를 찾는 검색에 쓴다. 리랭커가 짝으로 제공된다. | `text,image` → `embedding` | Apache-2.0 <sup>가중치</sup> | ✅ 가능 | gpu | [HF](https://huggingface.co/Qwen) · [논문](https://arxiv.org/abs/2601.04720) |

---

## 모델 조합

각 모델의 `inputs` / `outputs` 타입으로 연결 가능 여부가 결정됩니다. 
출력 타입이 다음 모델의 입력 타입에 포함될 때만 이어집니다.

**타입**  `text` · `image` · `video` · `audio` · `speech` · `boxes` · `mask` · `embedding` · `score`

### 예시 — 이미지를 설명하고 소리로 읽어주기

```
[image] ──▶ Qwen3-VL          ──▶ Kokoro        ──▶ [speech]
            inputs:  image,text     inputs:  text
            outputs: text           outputs: speech
```

두 모델 모두 상업 사용이 자유롭고 Kokoro 는 82M 이라 CPU 에서도 돕니다.

### 예시 — 음성 질문에 음성으로 답하기

```
[speech] ─▶ Whisper large-v3 ─▶ Qwen3.8-27B ─▶ Kokoro ─▶ [speech]
            speech→text          text→text       text→speech
```

### 타입이 맞지 않는 경우

```
[image] ─▶ YOLO26(→boxes) ─▶ Qwen3.8-27B(text→) ✕  boxes 를 받지 못함
[image] ─▶ Florence-2(→text) ─▶ Qwen3.8-27B(text→) ○
```

### 카테고리 연결 행렬

`dist/index.json` 의 타입 정보로 자동 생성됩니다. 숫자는 연결 가능한 모델 쌍의 수입니다.

| 앞 \ 뒤 | 대형 언어 모델 | 소형 언어 모델 | 비전-언어 모델 | 컴퓨터 비전 | 음성 인식 | 음성 합성 | 이미지 생성 | 영상 생성 | 임베딩·리랭킹 |
|---|---|---|---|---|---|---|---|---|---|
| 대형 언어 모델 | 42 | 7 | 28 | 14 | · | 35 | 28 | 35 | 28 |
| 소형 언어 모델 | 7 | · | 4 | 2 | · | 5 | 4 | 5 | 4 |
| 비전-언어 모델 | 28 | 4 | 12 | 8 | · | 20 | 16 | 20 | 16 |
| 컴퓨터 비전 | 14 | 2 | 8 | 3 | · | 10 | 8 | 10 | 8 |
| 음성 인식 | 35 | 5 | 20 | 10 | · | 25 | 20 | 25 | 20 |
| 음성 합성 | · | · | · | · | 25 | 12 | · | · | · |
| 이미지 생성 | · | · | 16 | 24 | · | · | 9 | 16 | 4 |
| 영상 생성 | · | · | · | 15 | · | · | · | · | · |
| 임베딩·리랭킹 | · | · | · | · | · | · | · | · | · |

---

## 기여

모델 추가는 [`data/`](data/) 의 해당 카테고리 YAML 에 항목을 더하고 검증을 돌리면 됩니다.

```bash
python3 scripts/validate.py   # 스키마·타입·중복 ID 검사
python3 scripts/build.py      # README.md + dist/index.json 재생성
```

필드 정의는 [SCHEMA.md](SCHEMA.md) 를 보세요. **모르는 값은 `null` 로 두고 추측하지 마세요.**

## 로드맵

- [x] **1단계** — 구조화된 모델 카탈로그 (지금)
- [ ] **2단계** — 성능 비교 웹사이트, 같은 입력에 대한 모델별 추론 결과 예시
- [ ] **3단계** — 블록·그래프 편집기로 모델을 조합해 프로덕트 구성
- [ ] **4단계** — 구성한 프로덕트를 로컬 실행 가능한 형태로 내려받기

---

<sub>카탈로그는 완전하지 않습니다. HuggingFace 에만 수백만 개 리포가 있고, 이 목록은 **용도별로 고를 수 있게 큐레이션한 것**입니다. 각 항목의 `sources` 필드에 근거 링크가 있습니다.</sub>
