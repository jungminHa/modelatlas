# 모델 카탈로그 스키마 v1

카탈로그의 원본은 `data/*.yaml`이다. `README.md`와 `dist/index.json`은
`scripts/build.py`가 여기서 **생성**한다. 수동으로 고치지 않는다.

---

## 왜 YAML 원본인가

"awesome-list" 형태의 마크다운 표는 링크 모음 이상이 되지 못한다.
이 프로젝트의 2~4단계(비교 웹사이트 · 블록 조합 · 로컬 실행)는
**기계가 읽을 수 있는 카탈로그**를 전제로 한다.

특히 3단계(모델 조합)가 성립하려면 각 모델이 **무엇을 받고 무엇을 내보내는지**
타입으로 선언되어 있어야 한다. 그래야 블록 편집기가 연결 가능 여부를 검증할 수 있다.
이 필드를 나중에 추가하면 카탈로그 전체를 다시 훑어야 하므로 처음부터 넣는다.

---

## 레코드 구조

```yaml
- id: qwen3-embedding-8b          # 전역 고유. 소문자·하이픈
  name: Qwen3-Embedding-8B
  category: embedding             # 아래 카테고리 표 참조
  task: text-embedding            # 세부 작업
  vendor: Alibaba

  # ── 조합 가능성 (3단계의 기반) ──
  inputs:  [text]
  outputs: [embedding]

  # ── 라이선스 (가장 자주 사고가 나는 지점) ──
  license: Apache-2.0
  openness: open-weight           # open-source | open-weight
  commercial_use: yes             # yes | no | conditional
  license_note: null

  # ── 실행 요건 ──
  params: 8B
  vram_min_gb: 16
  runs_on: [gpu]                  # cpu | gpu | edge | apple-silicon

  # ── 특화 (사용자가 고르는 근거) ──
  specialization: >
    100개 이상 언어 지원. 사용자 정의 지시문을 받아 도메인별로 동작을 조정할 수 있다.
  strengths: [multilingual, instruction-tunable]
  weaknesses: [gpu-required]

  # ── 링크·근거 ──
  links:
    huggingface: https://huggingface.co/Qwen/Qwen3-Embedding-8B
    github: null
    paper: https://arxiv.org/abs/2506.05176
  released: 2025-06
  benchmarks:
    - name: MTEB
      value: leading
      note: 2026-09 스냅샷 기준
  sources:
    - https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models
  verified: 2026-09-23
```

---

## 필수 필드

| 필드 | 필수 | 설명 |
|---|---|---|
| `id` | ✔ | 전역 고유 식별자 |
| `name` | ✔ | 표기명 |
| `category` | ✔ | 카테고리 |
| `inputs` / `outputs` | ✔ | **타입 목록. 조합 검증의 근거** |
| `license` | ✔ | SPDX 식별자 또는 라이선스명 |
| `openness` | ✔ | `open-source`(OSI 승인) / `open-weight` |
| `commercial_use` | ✔ | `yes` / `no` / `conditional` |
| `specialization` | ✔ | 무엇에 특화됐는가 (한 문단) |
| `sources` | ✔ | 정보 출처 URL |

**모르는 값은 `null`로 둔다.** 추측해서 채우지 않는다 —
VRAM 요건이나 라이선스를 잘못 적으면 사용자가 실제로 손해를 본다.

---

## 카테고리

| 카테고리 | 설명 |
|---|---|
| `llm` | 대형 언어 모델 (텍스트 생성·추론) |
| `slm` | 소형 언어 모델 (온디바이스·엣지) |
| `vlm` | 비전-언어 모델 (이미지 이해) |
| `vision` | 전통 컴퓨터 비전 (검출·분할·OCR) |
| `asr` | 음성 인식 |
| `tts` | 음성 합성 |
| `image-gen` | 이미지 생성 |
| `video-gen` | 영상 생성 |
| `embedding` | 임베딩·리랭킹 |
| `agent` | 에이전트 특화 모델·프레임워크 |

## 입출력 타입

블록 편집기는 **출력 타입이 입력 타입에 포함될 때만** 연결을 허용한다.

| 타입 | 설명 |
|---|---|
| `text` | 자연어 텍스트 |
| `image` | 정지 이미지 |
| `video` | 영상 |
| `audio` | 일반 오디오 |
| `speech` | 음성 (ASR 입력 / TTS 출력) |
| `boxes` | 바운딩 박스 목록 |
| `mask` | 분할 마스크 |
| `embedding` | 벡터 |
| `score` | 점수·순위 (리랭커 출력) |

### 조합 예시

사용자가 요청한 시나리오 — *이미지를 넣으면 설명하고 음성으로 읽어준다* — 는
타입만으로 검증된다.

```
[image] → VLM(inputs:[image,text] outputs:[text])
        → TTS(inputs:[text] outputs:[speech]) → [speech]
```

`vision` 모델을 앞에 넣는 변형도 타입이 맞으면 허용된다.

```
[image] → 검출(outputs:[boxes]) → LLM(inputs:[text]) ✕  타입 불일치
[image] → VLM(outputs:[text])   → LLM(inputs:[text]) ○
```

---

## 라이선스를 1급 필드로 둔 이유

가장 흔한 사고가 여기서 난다. 예를 들어 **XTTS-v2는 HuggingFace 최다 다운로드
TTS 모델이지만 Coqui Public Model License로 비상업 용도만 허용**한다.
모르고 제품에 넣으면 나중에 전부 걷어내야 한다.

또한 널리 쓰이는 모델 대부분(Llama, Qwen, Gemma, DeepSeek, Kimi, GLM)은
**OSI 기준 오픈소스가 아니라 open-weight**다. 이 구분을 `openness` 필드로 명시한다.

---

## 검증

```bash
python3 scripts/validate.py      # 스키마·타입·중복 ID 검사
python3 scripts/build.py         # README.md + dist/index.json 생성
```
