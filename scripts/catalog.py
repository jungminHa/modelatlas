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
# Redistribution is a SEPARATE permission from use. A model can be free to use
# commercially and still forbid rehosting the weights, and vice versa.
REDISTRIBUTABLE = {"yes","no","copyleft","check"}

# Keys that must be present but may hold null.
# Matches the SCHEMA.md rule: leave unknown values null rather than guessing.
NULLABLE_REQUIRED = {"license"}
REQUIRED = ["id","name","category","inputs","outputs","license","openness",
            "commercial_use","specialization","sources"]
OPTIONAL_ENUMS = {"redistributable": REDISTRIBUTABLE}


# Fields whose vocabulary includes bare yes/no and therefore hits the YAML trap
YESNO_FIELDS = ("commercial_use", "redistributable")


def _norm_yesno(v):
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
            for k in YESNO_FIELDS:
                if k in m:
                    m[k] = _norm_yesno(m[k])
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


# ─────────────────────────────────────────────────────────────
# VRAM estimation
#
# Where a vendor or a benchmark states a figure we use it (vram_min_gb).
# Otherwise we estimate from total parameter count:
#
#     vram_gb = params_b × bytes_per_param × 1.2
#
# The 1.2 covers activations and a modest KV cache. Bytes per parameter
# follow the usual quantization levels. This is an ESTIMATE and is always
# labelled as such — never presented as a measured requirement.
#
# For mixture-of-experts models the TOTAL parameter count drives VRAM, not
# the active count: every expert has to be resident to be routed to.
# ─────────────────────────────────────────────────────────────

BYTES_PER_PARAM = {"fp16": 2.0, "int8": 1.0, "int4": 0.55}
OVERHEAD = 1.2


def estimate_vram(params_b, precision="int4"):
    """Estimated GB of VRAM for a model of `params_b` billion parameters."""
    if not params_b:
        return None
    return round(params_b * BYTES_PER_PARAM[precision] * OVERHEAD, 1)


def vram_requirement(m, precision="int4"):
    """(gb, source) — source is 'stated' or 'estimated'; (None, None) if unknown."""
    stated = m.get("vram_min_gb")
    if stated is not None and stated > 0:
        return float(stated), "stated"
    est = estimate_vram(m.get("params_b"), precision)
    return (est, "estimated") if est else (None, None)
