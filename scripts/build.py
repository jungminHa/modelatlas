#!/usr/bin/env python3
"""카탈로그 → README.md + dist/index.json 생성.

README 는 사람이, index.json 은 웹사이트(2단계)와 블록 편집기(3단계)가 읽는다.
둘 다 data/*.yaml 에서 파생되므로 수동 편집하지 않는다.
"""
import sys, os, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import (load, by_category, can_connect, ROOT,
                     CATEGORIES, CATEGORY_KO, TYPES)

BADGE = {"yes": "✅ 가능", "no": "❌ 불가", "conditional": "⚠️ 조건부"}
OPEN  = {"open-source": "OSI", "open-weight": "가중치"}


def link_cell(m):
    l = m.get("links") or {}
    parts = []
    if l.get("huggingface"): parts.append(f'[HF]({l["huggingface"]})')
    if l.get("github"):      parts.append(f'[GH]({l["github"]})')
    if l.get("paper"):       parts.append(f'[논문]({l["paper"]})')
    return " · ".join(parts) or "—"


def io_cell(m):
    return f'`{",".join(m.get("inputs") or [])}` → `{",".join(m.get("outputs") or [])}`'


def build_readme(models):
    cats = by_category(models)
    n = len(models)
    commercial_ok = sum(1 for m in models if m["commercial_use"] == "yes")
    unverified = sum(1 for m in models if not m.get("license"))

    L = []
    A = L.append
    A("# ModelAtlas")
    A("")
    A("> 공개된 오픈소스·오픈웨이트 AI 모델을 **용도별로 찾고, 라이선스를 확인하고, 조합해서 쓰기** 위한 카탈로그.")
    A("")
    A(f"**모델 {n}개 · 카테고리 {len(cats)}개** · 최종 갱신 2026-09-23")
    A("")
    A("| | |")
    A("|---|---|")
    A(f"| 상업 사용 자유 | {commercial_ok}개 |")
    A(f"| 조건부·불가 | {n - commercial_ok}개 |")
    A(f"| 라이선스 미확인 | {unverified}개 |")
    A("")
    A("---")
    A("")
    A("## 이 카탈로그가 다른 점")
    A("")
    A("**1. 링크 모음이 아니라 구조화된 데이터입니다.**  ")
    A("원본은 [`data/*.yaml`](data/)이고 이 README 와 [`dist/index.json`](dist/index.json)은 거기서 생성됩니다.")
    A("")
    A("**2. 모델마다 입출력 타입이 선언되어 있습니다.**  ")
    A("그래서 *어떤 모델을 어떤 모델 뒤에 붙일 수 있는지* 기계가 판정합니다. 아래 조합 예시 참조.")
    A("")
    A("**3. 라이선스를 1급 정보로 다룹니다.**  ")
    A("가장 흔한 사고가 여기서 납니다. 예를 들어 **XTTS-v2 는 HuggingFace 최다 다운로드 TTS 모델이지만 비상업 용도만 허용**합니다. ")
    A("또한 널리 쓰이는 모델 대부분(Llama·Qwen·Gemma·DeepSeek·Kimi·GLM)은 OSI 기준 오픈소스가 아니라 **오픈웨이트**입니다.")
    A("")
    A("**4. 모르는 값은 비워 둡니다.**  ")
    A("VRAM 요건이나 라이선스를 추측해서 적으면 사용자가 실제로 손해를 봅니다. 미확인은 `—` 로 표시됩니다.")
    A("")
    A("---")
    A("")

    # ── 목차
    A("## 카테고리")
    A("")
    for c in CATEGORIES:
        if c in cats:
            A(f"- [{CATEGORY_KO[c]} ({len(cats[c])})](#{c})")
    A("")
    A("---")
    A("")

    # ── 카테고리별 표
    for c in CATEGORIES:
        if c not in cats:
            continue
        A(f'<a id="{c}"></a>')
        A("")
        A(f"## {CATEGORY_KO[c]}")
        A("")
        A("| 모델 | 특화 | 입력 → 출력 | 라이선스 | 상업 | 실행 | 링크 |")
        A("|---|---|---|---|---|---|---|")
        for m in sorted(cats[c], key=lambda x: x["name"]):
            spec = " ".join((m.get("specialization") or "").split())
            if len(spec) > 90:
                spec = spec[:88] + "…"
            lic = m.get("license") or "—"
            if m.get("openness"):
                lic += f' <sup>{OPEN[m["openness"]]}</sup>'
            vram = m.get("vram_min_gb")
            run = ", ".join(m.get("runs_on") or []) or "—"
            if vram not in (None, ""):
                run += f" · {vram}GB+" if vram else " · CPU"
            A(f'| **{m["name"]}** | {spec} | {io_cell(m)} | {lic} | '
              f'{BADGE.get(m["commercial_use"], "—")} | {run} | {link_cell(m)} |')
        A("")

    # ── 조합
    A("---")
    A("")
    A("## 모델 조합")
    A("")
    A("각 모델의 `inputs` / `outputs` 타입으로 연결 가능 여부가 결정됩니다. ")
    A("출력 타입이 다음 모델의 입력 타입에 포함될 때만 이어집니다.")
    A("")
    A("**타입**  " + " · ".join(f"`{t}`" for t in TYPES))
    A("")
    A("### 예시 — 이미지를 설명하고 소리로 읽어주기")
    A("")
    A("```")
    A("[image] ──▶ Qwen3-VL          ──▶ Kokoro        ──▶ [speech]")
    A("            inputs:  image,text     inputs:  text")
    A("            outputs: text           outputs: speech")
    A("```")
    A("")
    A("두 모델 모두 상업 사용이 자유롭고 Kokoro 는 82M 이라 CPU 에서도 돕니다.")
    A("")
    A("### 예시 — 음성 질문에 음성으로 답하기")
    A("")
    A("```")
    A("[speech] ─▶ Whisper large-v3 ─▶ Qwen3.8-27B ─▶ Kokoro ─▶ [speech]")
    A("            speech→text          text→text       text→speech")
    A("```")
    A("")
    A("### 타입이 맞지 않는 경우")
    A("")
    A("```")
    A("[image] ─▶ YOLO26(→boxes) ─▶ Qwen3.8-27B(text→) ✕  boxes 를 받지 못함")
    A("[image] ─▶ Florence-2(→text) ─▶ Qwen3.8-27B(text→) ○")
    A("```")
    A("")

    # 자동 산출: 카테고리 간 연결 가능 행렬
    A("### 카테고리 연결 행렬")
    A("")
    A("`dist/index.json` 의 타입 정보로 자동 생성됩니다. 숫자는 연결 가능한 모델 쌍의 수입니다.")
    A("")
    order = [c for c in CATEGORIES if c in cats]
    A("| 앞 \\ 뒤 | " + " | ".join(CATEGORY_KO[c] for c in order) + " |")
    A("|---" * (len(order) + 1) + "|")
    for a in order:
        row = [CATEGORY_KO[a]]
        for b in order:
            cnt = sum(1 for x in cats[a] for y in cats[b]
                      if x["id"] != y["id"] and can_connect(x, y))
            row.append(str(cnt) if cnt else "·")
        A("| " + " | ".join(row) + " |")
    A("")

    A("---")
    A("")
    A("## 기여")
    A("")
    A("모델 추가는 [`data/`](data/) 의 해당 카테고리 YAML 에 항목을 더하고 검증을 돌리면 됩니다.")
    A("")
    A("```bash")
    A("python3 scripts/validate.py   # 스키마·타입·중복 ID 검사")
    A("python3 scripts/build.py      # README.md + dist/index.json 재생성")
    A("```")
    A("")
    A("필드 정의는 [SCHEMA.md](SCHEMA.md) 를 보세요. **모르는 값은 `null` 로 두고 추측하지 마세요.**")
    A("")
    A("## 로드맵")
    A("")
    A("- [x] **1단계** — 구조화된 모델 카탈로그 (지금)")
    A("- [ ] **2단계** — 성능 비교 웹사이트, 같은 입력에 대한 모델별 추론 결과 예시")
    A("- [ ] **3단계** — 블록·그래프 편집기로 모델을 조합해 프로덕트 구성")
    A("- [ ] **4단계** — 구성한 프로덕트를 로컬 실행 가능한 형태로 내려받기")
    A("")
    A("---")
    A("")
    A("<sub>카탈로그는 완전하지 않습니다. HuggingFace 에만 수백만 개 리포가 있고, 이 목록은 "
      "**용도별로 고를 수 있게 큐레이션한 것**입니다. 각 항목의 `sources` 필드에 근거 링크가 있습니다.</sub>")
    return "\n".join(L) + "\n"


def build_index(models):
    cats = by_category(models)
    # 연결 가능 쌍을 미리 계산해 두면 편집기가 그래프만 읽으면 된다
    edges = [{"from": a["id"], "to": b["id"],
              "types": sorted(set(a["outputs"]) & set(b["inputs"]))}
             for a in models for b in models
             if a["id"] != b["id"] and can_connect(a, b)]
    return {
        "version": 1,
        "generated": "2026-09-23",
        "counts": {"models": len(models), "categories": len(cats), "edges": len(edges)},
        "types": TYPES,
        "categories": [{"id": c, "name_ko": CATEGORY_KO[c], "count": len(cats[c])}
                       for c in CATEGORIES if c in cats],
        "models": [{k: v for k, v in m.items() if not k.startswith("_")} for m in models],
        "edges": edges,
    }


def main():
    models, files = load()
    readme = build_readme(models)
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(readme)
    idx = build_index(models)
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    # YAML 이 날짜 문자열을 date 객체로 읽으므로 직렬화 시 되돌린다
    def _ser(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        raise TypeError(f"직렬화 불가: {type(o).__name__}")
    json.dump(idx, open(os.path.join(ROOT, "dist", "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=_ser)
    print(f"README.md      {len(readme.splitlines()):,}줄")
    print(f"dist/index.json 모델 {idx['counts']['models']}개 · "
          f"연결 가능 쌍 {idx['counts']['edges']:,}개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
