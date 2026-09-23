#!/usr/bin/env python3
"""Check which catalog models your machine can actually run.

    python3 scripts/check_env.py                 # summary
    python3 scripts/check_env.py --all           # every model, including ones that fit
    python3 scripts/check_env.py --precision int8
    python3 scripts/check_env.py --json

Detects GPU / unified memory and compares it against each model's VRAM
requirement. Requirements are either stated by the vendor or estimated from
parameter count — the output always says which.

No models are downloaded and nothing is sent anywhere.
"""
import sys, os, json, platform, subprocess, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import (load, by_category, CATEGORIES, CATEGORY_NAMES,
                     vram_requirement, estimate_vram, BYTES_PER_PARAM)

# macOS caps the GPU working set well below total unified memory.
# 0.75 is the conventional safe fraction; iogpu.wired_limit_mb can raise it.
APPLE_GPU_FRACTION = 0.75
# CPU-only inference still needs headroom for the OS and the runtime.
CPU_FRACTION = 0.70


def _sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True,
                              text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def _true_arch():
    """platform.machine() reports x86_64 when Python itself runs under Rosetta.
    hw.optional.arm64 reports the real CPU, so prefer it on macOS."""
    if platform.system() == "Darwin" and _sh("sysctl -n hw.optional.arm64") == "1":
        return "arm64"
    return platform.machine()


def detect():
    arch = _true_arch()
    env = {
        "os": platform.system(),
        "release": platform.mac_ver()[0] or platform.release(),
        "arch": arch,
        "python": platform.python_version(),
        "python_arch": platform.machine(),
        "cpu": None, "ram_gb": None,
        "accelerator": None, "gpu_name": None,
        "vram_gb": None, "vram_kind": None, "budget_gb": None,
        "notes": [],
    }

    # ── NVIDIA ──
    nv = _sh("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits")
    if nv:
        first = nv.split("\n")[0].split(",")
        env["accelerator"] = "cuda"
        env["gpu_name"] = first[0].strip()
        try:
            env["vram_gb"] = round(float(first[1]) / 1024, 1)
        except Exception:
            pass
        env["vram_kind"] = "dedicated VRAM"
        if len(nv.split("\n")) > 1:
            env["notes"].append(f"{len(nv.split(chr(10)))} GPUs detected; "
                                f"only the first is used for this check")

    # ── Apple Silicon ──
    elif env["os"] == "Darwin" and arch == "arm64":
        env["accelerator"] = "mps"
        env["gpu_name"] = _sh("sysctl -n machdep.cpu.brand_string") or "Apple Silicon"
        cores = _sh("system_profiler SPDisplaysDataType 2>/dev/null | "
                    "grep 'Total Number of Cores' | head -1 | awk '{print $NF}'")
        if cores:
            env["gpu_name"] += f" ({cores}-core GPU)"
        env["vram_kind"] = "unified memory"

    # ── AMD ROCm ──
    elif _sh("command -v rocm-smi"):
        env["accelerator"] = "rocm"
        env["gpu_name"] = "AMD GPU"
        env["vram_kind"] = "dedicated VRAM"

    # ── RAM / CPU ──
    mem = _sh("sysctl -n hw.memsize") or _sh("grep MemTotal /proc/meminfo | awk '{print $2*1024}'")
    if mem:
        try:
            env["ram_gb"] = round(int(float(mem)) / 1024**3)
        except Exception:
            pass
    env["cpu"] = _sh("sysctl -n machdep.cpu.brand_string") or platform.processor() or "unknown"

    # ── Budget ──
    if env["accelerator"] == "mps" and env["ram_gb"]:
        env["vram_gb"] = env["ram_gb"]
        env["budget_gb"] = round(env["ram_gb"] * APPLE_GPU_FRACTION, 1)
        env["notes"].append(
            f"Unified memory: the GPU shares the {env['ram_gb']}GB with the OS. "
            f"Budget assumes {int(APPLE_GPU_FRACTION*100)}% is usable.")
    elif env["vram_gb"]:
        env["budget_gb"] = env["vram_gb"]
    elif env["ram_gb"]:
        env["accelerator"] = env["accelerator"] or "cpu"
        env["budget_gb"] = round(env["ram_gb"] * CPU_FRACTION, 1)
        env["notes"].append("No GPU detected — budget is system RAM for CPU inference, "
                            "which is far slower.")
    return env


def platform_supported(m, env):
    """Does the model claim to run on this accelerator? Returns (ok, note)."""
    runs = set(m.get("runs_on") or [])
    if not runs:
        return None, "runs_on not recorded"
    acc = env["accelerator"]
    if acc == "mps":
        if "apple-silicon" in runs:
            return True, None
        if "cpu" in runs:
            return True, "listed for CPU; Apple GPU support not confirmed"
        if "gpu" in runs:
            return None, "listed for GPU but Apple Silicon support not confirmed"
    if acc == "cuda" and ("gpu" in runs or "edge" in runs):
        return True, None
    if acc == "cpu":
        return ("cpu" in runs or "edge" in runs), None
    return None, None


def assess(m, env, precision):
    need, src = vram_requirement(m, precision)
    budget = env["budget_gb"]
    plat_ok, plat_note = platform_supported(m, env)

    if need is None:
        status = "unknown"
    elif budget is None:
        status = "unknown"
    elif need <= budget * 0.85:
        status = "fits"
    elif need <= budget:
        status = "tight"
    else:
        status = "too-big"

    # Would a smaller quantization help?
    alt = None
    if status == "too-big" and m.get("params_b") and budget:
        for p in ("int8", "int4"):
            if estimate_vram(m["params_b"], p) <= budget:
                alt = p
                break

    if status in ("fits", "tight") and plat_ok is False:
        status = "unsupported-platform"
    return {"need_gb": need, "need_source": src, "status": status,
            "alt_precision": alt, "platform_note": plat_note}


ICON = {"fits": "✅", "tight": "⚠️ ", "too-big": "❌", "unknown": "❓",
        "unsupported-platform": "🚫"}
LABEL = {"fits": "runs", "tight": "tight", "too-big": "too large",
         "unknown": "unknown", "unsupported-platform": "platform"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--precision", default="int4", choices=list(BYTES_PER_PARAM))
    ap.add_argument("--all", action="store_true", help="list every model")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    env = detect()
    models, _ = load()
    results = {m["id"]: assess(m, env, a.precision) for m in models}

    if a.json:
        print(json.dumps({"environment": env, "precision": a.precision,
                          "results": results}, indent=1, ensure_ascii=False))
        return 0

    W = 76
    print("=" * W)
    print("  Environment check")
    print("=" * W)
    print(f"  OS           {env['os']} {env['release']} ({env['arch']})")
    if env.get("python_arch") and env["python_arch"] != env["arch"]:
        print(f"  ⚠  Python    {env['python']} is {env['python_arch']} running under "
              f"Rosetta on {env['arch']}")
        print(f"               GPU acceleration needs a native {env['arch']} Python")
    print(f"  CPU          {env['cpu']}")
    print(f"  RAM          {env['ram_gb']}GB" if env["ram_gb"] else "  RAM          unknown")
    print(f"  Accelerator  {env['accelerator'] or 'none'}"
          + (f" — {env['gpu_name']}" if env["gpu_name"] else ""))
    if env["vram_gb"]:
        print(f"  {env['vram_kind']:<13} {env['vram_gb']}GB"
              f"  →  usable budget {env['budget_gb']}GB")
    for n in env["notes"]:
        print(f"  note         {n}")
    print(f"\n  Comparing against {a.precision} weights "
          f"(change with --precision int8|fp16)")

    tally = {}
    for r in results.values():
        tally[r["status"]] = tally.get(r["status"], 0) + 1
    print(f"\n{'=' * W}\n  Summary — {len(models)} models\n{'=' * W}\n")
    for k in ("fits", "tight", "too-big", "unsupported-platform", "unknown"):
        if tally.get(k):
            bar = "█" * round(tally[k] / len(models) * 34)
            print(f"  {ICON[k]} {LABEL[k]:<12}{tally[k]:>3}  {bar}")

    print(f"\n{'=' * W}\n  By category\n{'=' * W}")
    cats = by_category(models)
    unconfirmed = set()
    for c in CATEGORIES:
        if c not in cats:
            continue
        rows = [(m, results[m["id"]]) for m in sorted(cats[c], key=lambda x: x["name"])]
        shown = rows if a.all else [r for r in rows if r[1]["status"] != "too-big"]
        n_big = sum(1 for _, r in rows if r["status"] == "too-big")
        print(f"\n  {CATEGORY_NAMES[c]}"
              + ("" if a.all or not n_big else f"   ({n_big} too large, hidden — use --all)"))
        if not shown:
            print("     nothing runs here on this machine")
            continue
        for m, r in shown:
            need = f"{r['need_gb']}GB" if r["need_gb"] else "—"
            tag = "~" if r["need_source"] == "estimated" else " "
            line = f"     {ICON[r['status']]} {m['name']:<26}{tag}{need:>8}"
            if r["alt_precision"]:
                line += f"   fits at {r['alt_precision']}"
            if r["platform_note"]:
                unconfirmed.add(m["id"])
                line += " *"
            print(line)

    print(f"\n{'=' * W}")
    if unconfirmed:
        print(f"  * {len(unconfirmed)} models are recorded as GPU/CPU without naming")
        print(f"    {env['accelerator']} specifically. Memory may fit, but framework")
        print(f"    support has to be checked per model. Improving the runs_on field")
        print(f"    in data/ is the fix — see CONTRIBUTING.md.")
        print()
    print("  ~ before a figure means it is estimated from parameter count,")
    print("    not a measured requirement. Unknown (❓) means neither a stated")
    print("    figure nor a parameter count is recorded — see SCHEMA.md.")
    print("  Fitting in memory is necessary, not sufficient: throughput,")
    print("    framework support and context length all still apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
