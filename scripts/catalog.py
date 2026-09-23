# -*- coding: utf-8 -*-
"""카탈로그 로더 — validate.py 와 build.py 가 공유한다."""
import os, glob
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

CATEGORIES = ["llm","slm","vlm","vision","asr","tts","image-gen","video-gen","embedding","agent"]
CATEGORY_KO = {
    "llm":"대형 언어 모델", "slm":"소형 언어 모델", "vlm":"비전-언어 모델",
    "vision":"컴퓨터 비전", "asr":"음성 인식", "tts":"음성 합성",
    "image-gen":"이미지 생성", "video-gen":"영상 생성",
    "embedding":"임베딩·리랭킹", "agent":"에이전트",
}
TYPES = ["text","image","video","audio","speech","boxes","mask","embedding","score"]
OPENNESS = {"open-source","open-weight"}
COMMERCIAL = {"yes","no","conditional"}

# 키는 반드시 있어야 하지만 값이 null 이어도 되는 필드.
# SCHEMA.md 의 "모르는 값은 null 로 둔다" 원칙과 일치시킨다.
NULLABLE_REQUIRED = {"license"}
REQUIRED = ["id","name","category","inputs","outputs","license","openness",
            "commercial_use","specialization","sources"]


def _norm_commercial(v):
    """YAML 1.1 은 bare yes/no 를 불리언으로 읽는다. 기여자도 반드시 같은 실수를 하므로
    데이터를 고치는 대신 로더에서 흡수한다."""
    if v is True:  return "yes"
    if v is False: return "no"
    return str(v) if v is not None else None


def load():
    models, files = [], sorted(glob.glob(os.path.join(DATA, "*.yaml")))
    for f in files:
        for m in (yaml.safe_load(open(f, encoding="utf-8")) or []):
            m["_file"] = os.path.basename(f)
            m["commercial_use"] = _norm_commercial(m.get("commercial_use"))
            m.setdefault("links", {}) or m.__setitem__("links", m.get("links") or {})
            models.append(m)
    return models, files


def by_category(models):
    out = {c: [] for c in CATEGORIES}
    for m in models:
        out.setdefault(m.get("category"), []).append(m)
    return {c: v for c, v in out.items() if v}


def can_connect(a, b):
    """a 의 출력이 b 의 입력에 하나라도 맞으면 연결 가능."""
    return bool(set(a.get("outputs") or []) & set(b.get("inputs") or []))
