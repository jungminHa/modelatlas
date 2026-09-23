# -*- coding: utf-8 -*-
"""Catalog loader — shared by validate.py and build.py."""
import os, glob
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

CATEGORIES = ["llm","slm","vlm","vision","asr","tts","image-gen","video-gen","embedding","agent"]
CATEGORY_NAMES = {
    "llm": "Large Language Models",
    "slm": "Small Language Models",
    "vlm": "Vision-Language Models",
    "vision": "Computer Vision",
    "asr": "Speech Recognition",
    "tts": "Text to Speech",
    "image-gen": "Image Generation",
    "video-gen": "Video Generation",
    "embedding": "Embedding & Reranking",
    "agent": "Agents",
}
TYPES = ["text","image","video","audio","speech","boxes","mask","embedding","score"]
OPENNESS = {"open-source","open-weight"}
COMMERCIAL = {"yes","no","conditional"}

# Keys that must be present but may hold null.
# Matches the SCHEMA.md rule: leave unknown values null rather than guessing.
NULLABLE_REQUIRED = {"license"}
REQUIRED = ["id","name","category","inputs","outputs","license","openness",
            "commercial_use","specialization","sources"]


def _norm_commercial(v):
    """YAML 1.1 parses bare yes/no as booleans. Contributors will hit this too,
    so absorb it in the loader instead of quoting every value in the data."""
    if v is True:  return "yes"
    if v is False: return "no"
    return str(v) if v is not None else None


def load():
    models, files = [], sorted(glob.glob(os.path.join(DATA, "*.yaml")))
    for f in files:
        for m in (yaml.safe_load(open(f, encoding="utf-8")) or []):
            m["_file"] = os.path.basename(f)
            m["commercial_use"] = _norm_commercial(m.get("commercial_use"))
            m["links"] = m.get("links") or {}
            models.append(m)
    return models, files


def by_category(models):
    out = {c: [] for c in CATEGORIES}
    for m in models:
        out.setdefault(m.get("category"), []).append(m)
    return {c: v for c, v in out.items() if v}


def can_connect(a, b):
    """Connectable when any output type of `a` is accepted as an input of `b`."""
    return bool(set(a.get("outputs") or []) & set(b.get("inputs") or []))
