#!/usr/bin/env python3
"""Generate README.md and dist/index.json from the catalog.

The README is for people; index.json is consumed by the comparison site (step 2)
and the block editor (step 3). Both are derived from data/*.yaml — never edit by hand.
"""
import sys, os, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import (load, by_category, can_connect, ROOT,
                     CATEGORIES, CATEGORY_NAMES, TYPES)

BADGE = {"yes": "✅ Yes", "no": "❌ No", "conditional": "⚠️ Conditional"}
OPEN  = {"open-source": "OSI", "open-weight": "weights"}


def link_cell(m):
    l = m.get("links") or {}
    parts = []
    if l.get("huggingface"): parts.append(f'[HF]({l["huggingface"]})')
    if l.get("github"):      parts.append(f'[GH]({l["github"]})')
    if l.get("paper"):       parts.append(f'[paper]({l["paper"]})')
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
    A("> A catalog of open-source and open-weight AI models — **find them by what they do, "
      "check the license, and compose them into pipelines.**")
    A("")
    A(f"**{n} models · {len(cats)} categories** · last updated 2026-09-23")
    A("")
    A("| | |")
    A("|---|---|")
    A(f"| Free for commercial use | {commercial_ok} |")
    A(f"| Conditional or prohibited | {n - commercial_ok} |")
    A(f"| License unverified | {unverified} |")
    A("")
    A("---")
    A("")
    A("## What makes this different")
    A("")
    A("**1. Structured data, not a link list.**  ")
    A("The source of truth is [`data/*.yaml`](data/). This README and "
      "[`dist/index.json`](dist/index.json) are generated from it.")
    A("")
    A("**2. Every model declares its input and output types.**  ")
    A("That is what lets a machine decide *which model can follow which*. See "
      "[Composing models](#composing-models) below.")
    A("")
    A("**3. Licensing is a first-class field.**  ")
    A("This is where people get burned. **XTTS-v2 is the most-downloaded TTS model on "
      "Hugging Face, yet its weights are non-commercial only.** And most widely used models "
      "(Llama, Qwen, Gemma, DeepSeek, Kimi, GLM) are **open-weight, not OSI open-source** — "
      "the `openness` field records that distinction.")
    A("")
    A("**4. Unknown values are left empty.**  ")
    A("Guessing a VRAM requirement or a license costs the reader real money. "
      "Unverified fields show as `—` and the validator flags them.")
    A("")
    A("---")
    A("")

    A("## Categories")
    A("")
    for c in CATEGORIES:
        if c in cats:
            A(f"- [{CATEGORY_NAMES[c]} ({len(cats[c])})](#{c})")
    A("")
    A("---")
    A("")

    for c in CATEGORIES:
        if c not in cats:
            continue
        A(f'<a id="{c}"></a>')
        A("")
        A(f"## {CATEGORY_NAMES[c]}")
        A("")
        A("| Model | Best at | In → Out | License | Commercial | Runs on | Links |")
        A("|---|---|---|---|---|---|---|")
        for m in sorted(cats[c], key=lambda x: x["name"]):
            spec = " ".join((m.get("specialization") or "").split())
            if len(spec) > 110:
                spec = spec[:108] + "…"
            lic = m.get("license") or "—"
            if m.get("openness"):
                lic += f' <sup>{OPEN[m["openness"]]}</sup>'
            vram = m.get("vram_min_gb")
            run = ", ".join(m.get("runs_on") or []) or "—"
            if vram:
                run += f" · {vram}GB+"
            A(f'| **{m["name"]}** | {spec} | {io_cell(m)} | {lic} | '
              f'{BADGE.get(m["commercial_use"], "—")} | {run} | {link_cell(m)} |')
        A("")

    A("---")
    A("")
    A("## Getting the weights")
    A("")
    A("```bash")
    A("python3 scripts/fetch.py --list       # what can be fetched")
    A("python3 scripts/fetch.py kokoro       # download into models/")
    A("python3 scripts/fetch.py --status     # what is already local")
    A("```")
    A("")
    A("**This repository does not host model weights.** `fetch.py` pulls from the original "
      "publisher into a local `models/` directory that is gitignored, and prints the "
      "license terms before downloading anything.")
    A("")
    A("That is a deliberate choice, not a limitation:")
    A("")
    A("- **Licensing** — redistributing weights is a separate permission from using them. "
      "XTTS-v2 forbids it; Llama and Gemma attach conditions.")
    A("- **Size** — the entries with a known parameter count total roughly **9.5 TB** at "
      "fp16. Kimi K3 alone is about 5.6 TB.")
    A("- **Platform limits** — GitHub blocks files over 100 MiB; Git LFS on Free/Pro "
      "includes 10 GiB of storage and bandwidth.")
    A("")
    A("`models/manifest.json` records the exact revision of everything you fetched and *is* "
      "committed, so a setup can be reproduced without shipping the weights.")
    A("")
    A("---")
    A("")
    A("## Will it run on my machine?")
    A("")
    A("```bash")
    A("python3 scripts/check_env.py")
    A("```")
    A("")
    A("Detects your GPU or unified memory and reports, per model, whether it fits. "
      "Nothing is downloaded and nothing leaves your machine.")
    A("")
    A("```")
    A("Accelerator  mps — Apple M1 Pro (14-core GPU)")
    A("unified memory 16GB  →  usable budget 12.0GB")
    A("")
    A("✅ runs          5")
    A("❌ too large    10")
    A("❓ unknown      26")
    A("```")
    A("")
    A("Requirements come from `vram_min_gb` when a figure has been published, and are "
      "otherwise estimated from `params_b` — estimates are printed with a `~` so they are "
      "never mistaken for measured values. For mixture-of-experts models the **total** "
      "parameter count drives memory, not the active count: a 552B/8B-active model still "
      "needs all experts resident.")
    A("")
    A("`--all` includes models that do not fit, `--precision int8|fp16` changes the "
      "assumed quantization, and `--json` emits machine-readable output.")
    A("")
    A("---")
    A("")
    A('<a id="composing-models"></a>')
    A("")
    A("## Composing models")
    A("")
    A("Each model declares `inputs` and `outputs`. Two models connect only when an output "
      "type of the first appears in the inputs of the second.")
    A("")
    A("**Types**  " + " · ".join(f"`{t}`" for t in TYPES))
    A("")
    A("### Example — describe an image and read it aloud")
    A("")
    A("```")
    A("[image] ──▶ Qwen3-VL          ──▶ Kokoro        ──▶ [speech]")
    A("            inputs:  image,text     inputs:  text")
    A("            outputs: text           outputs: speech")
    A("```")
    A("")
    A("Both are free for commercial use, and Kokoro is 82M parameters so it runs on CPU.")
    A("")
    A("### Example — answer a spoken question with speech")
    A("")
    A("```")
    A("[speech] ─▶ Whisper large-v3 ─▶ Qwen3.8-27B ─▶ Kokoro ─▶ [speech]")
    A("            speech→text          text→text       text→speech")
    A("```")
    A("")
    A("### When types do not line up")
    A("")
    A("```")
    A("[image] ─▶ YOLO26 (→boxes)    ─▶ Qwen3.8-27B (text→)  ✕  cannot accept boxes")
    A("[image] ─▶ Florence-2 (→text) ─▶ Qwen3.8-27B (text→)  ○")
    A("```")
    A("")
    A("### Category connection matrix")
    A("")
    A("Generated from the type declarations. Each cell counts the connectable model pairs.")
    A("")
    order = [c for c in CATEGORIES if c in cats]
    A("| from \\ to | " + " | ".join(CATEGORY_NAMES[c] for c in order) + " |")
    A("|---" * (len(order) + 1) + "|")
    for a in order:
        row = [CATEGORY_NAMES[a]]
        for b in order:
            cnt = sum(1 for x in cats[a] for y in cats[b]
                      if x["id"] != y["id"] and can_connect(x, y))
            row.append(str(cnt) if cnt else "·")
        A("| " + " | ".join(row) + " |")
    A("")

    A("---")
    A("")
    A("## Contributing")
    A("")
    A("Add a model by appending an entry to the matching YAML file in [`data/`](data/), "
      "then run:")
    A("")
    A("```bash")
    A("python3 scripts/validate.py   # schema, types, duplicate ids")
    A("python3 scripts/build.py      # regenerate README.md and dist/index.json")
    A("```")
    A("")
    A("Field definitions are in [SCHEMA.md](SCHEMA.md). "
      "**Leave unknown values as `null` — do not guess.** "
      "See [CONTRIBUTING.md](CONTRIBUTING.md).")
    A("")
    A("## Roadmap")
    A("")
    A("- [x] **Step 1** — structured model catalog *(you are here)*")
    A("- [ ] **Step 2** — comparison site with side-by-side inference on the same input")
    A("- [ ] **Step 3** — block/graph editor to compose models into a product")
    A("- [ ] **Step 4** — export a composed pipeline that runs locally")
    A("")
    A("## License")
    A("")
    A("Catalog data and documentation: **CC BY 4.0**. Code under `scripts/`: **MIT**. "
      "See [LICENSE](LICENSE).")
    A("")
    A("Each listed model carries its own license — always check the model's own terms "
      "before use. The `license` field here is a pointer, not legal advice.")
    A("")
    A("---")
    A("")
    A("<sub>This catalog is curated, not exhaustive. Hugging Face alone hosts millions of "
      "repositories; a complete list would not help anyone choose. Every entry carries a "
      "`sources` field pointing at where its information came from.</sub>")
    return "\n".join(L) + "\n"


def build_index(models):
    cats = by_category(models)
    # Precompute connectable pairs so the editor only has to read the graph
    edges = [{"from": a["id"], "to": b["id"],
              "types": sorted(set(a["outputs"]) & set(b["inputs"]))}
             for a in models for b in models
             if a["id"] != b["id"] and can_connect(a, b)]
    return {
        "version": 1,
        "generated": "2026-09-23",
        "counts": {"models": len(models), "categories": len(cats), "edges": len(edges)},
        "types": TYPES,
        "categories": [{"id": c, "name": CATEGORY_NAMES[c], "count": len(cats[c])}
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
    # YAML reads date-like strings as date objects; convert back on serialization
    def _ser(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        raise TypeError(f"not serializable: {type(o).__name__}")
    json.dump(idx, open(os.path.join(ROOT, "dist", "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=_ser)
    print(f"README.md        {len(readme.splitlines()):,} lines")
    print(f"dist/index.json  {idx['counts']['models']} models · "
          f"{idx['counts']['edges']:,} connectable pairs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
