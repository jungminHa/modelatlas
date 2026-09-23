#!/usr/bin/env python3
"""Download catalog models to a local models/ directory.

    python3 scripts/fetch.py --list              # what can be fetched
    python3 scripts/fetch.py kokoro              # fetch one model
    python3 scripts/fetch.py kokoro whisper-large-v3
    python3 scripts/fetch.py kokoro --yes        # skip the license prompt
    python3 scripts/fetch.py --status            # what is already local

Weights are NOT redistributed by this repository. They are pulled from the
original publisher, so the publisher's license applies to your copy. This
script shows those terms before it downloads anything.

Downloads land in models/ which is gitignored. models/manifest.json records
the exact revision of everything fetched so a setup can be reproduced.
"""
import sys, os, json, argparse, shutil, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import load, ROOT, vram_requirement

MODELS_DIR = os.path.join(ROOT, "models")
MANIFEST = os.path.join(MODELS_DIR, "manifest.json")


def repo_id(m):
    """Extract a Hugging Face repo id from the catalog link.

    A link with two path segments is a model repo. One segment is an
    organization page, which cannot be fetched directly — those entries need
    an explicit repo_id in the data.
    """
    if m.get("repo_id"):
        return m["repo_id"]
    url = (m.get("links") or {}).get("huggingface")
    if not url:
        return None
    parts = [p for p in url.rstrip("/").split("huggingface.co/")[-1].split("/") if p]
    return "/".join(parts[:2]) if len(parts) >= 2 else None


def load_manifest():
    if os.path.exists(MANIFEST):
        try:
            return json.load(open(MANIFEST, encoding="utf-8"))
        except Exception:
            pass
    return {"version": 1, "models": {}}


def save_manifest(man):
    os.makedirs(MODELS_DIR, exist_ok=True)
    man["updated"] = datetime.datetime.now().strftime("%Y-%m-%d")
    json.dump(man, open(MANIFEST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def dir_size_gb(p):
    t = 0
    for root, _, files in os.walk(p):
        for f in files:
            try:
                t += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return round(t / 1024**3, 2)


def license_gate(m, auto_yes):
    """Show the terms. Returns True to proceed."""
    cu = m.get("commercial_use")
    lic = m.get("license") or "UNVERIFIED"
    print(f"\n  License   {lic}   ({m.get('openness')})")
    if m.get("license_note"):
        print(f"  Note      {m['license_note']}")

    if cu == "no":
        print("\n  ⛔ NON-COMMERCIAL ONLY")
        print("     Using these weights in a commercial product is a license violation.")
        print("     This repository does not redistribute them; you are downloading")
        print("     directly from the publisher and accepting their terms.")
    elif cu == "conditional":
        print("\n  ⚠️  CONDITIONAL commercial use — read the license before shipping.")
    elif not m.get("license"):
        print("\n  ⚠️  License not verified in this catalog. Check the model page yourself.")

    if auto_yes:
        return True
    if cu == "no":
        ans = input("\n  Type 'non-commercial' to confirm you understand: ").strip()
        return ans == "non-commercial"
    ans = input("\n  Proceed? [y/N] ").strip().lower()
    return ans in ("y", "yes")


def hardware_note(m):
    need, src = vram_requirement(m, "int4")
    if not need:
        return
    free = shutil.disk_usage(ROOT).free / 1024**3
    tilde = "~" if src == "estimated" else ""
    print(f"  Memory    {tilde}{need}GB at int4   ·   disk free {free:,.0f}GB")
    if need > free:
        print("  ⚠️  The weights are unlikely to fit on this disk.")


def fetch_one(m, args, man):
    rid = repo_id(m)
    print("\n" + "─" * 70)
    print(f"  {m['name']}   [{m['id']}]")
    print("─" * 70)
    if not rid:
        print("  ✕ No specific Hugging Face repo recorded for this model.")
        print("    The catalog links to an organization page. Add a `repo_id`")
        print("    field in data/ to make it fetchable — see CONTRIBUTING.md.")
        return False
    print(f"  Source    huggingface.co/{rid}")
    hardware_note(m)
    if not license_gate(m, args.yes):
        print("  ✕ Skipped.")
        return False

    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("\n  ✕ huggingface_hub is not installed:  pip install huggingface_hub")
        return False

    dest = os.path.join(MODELS_DIR, m["id"])
    print(f"\n  → {os.path.relpath(dest, ROOT)}/")
    try:
        path = snapshot_download(repo_id=rid, local_dir=dest,
                                 allow_patterns=args.include or None)
    except Exception as e:
        msg = str(e)
        print(f"\n  ✕ Download failed: {type(e).__name__}")
        if "401" in msg or "403" in msg or "gated" in msg.lower():
            print("    This repo is gated. Accept the terms on the model page,")
            print("    then authenticate:  hf auth login")
        else:
            print(f"    {msg.splitlines()[0][:120]}")
        return False

    size = dir_size_gb(path)
    rev = None
    ref = os.path.join(dest, ".cache", "huggingface", "download")
    try:
        from huggingface_hub import HfApi
        rev = HfApi().model_info(rid).sha
    except Exception:
        pass
    man["models"][m["id"]] = {
        "repo_id": rid, "revision": rev, "size_gb": size,
        "license": m.get("license"), "commercial_use": m.get("commercial_use"),
        "fetched": datetime.datetime.now().strftime("%Y-%m-%d"),
    }
    save_manifest(man)
    print(f"  ✓ {size}GB   revision {rev[:12] if rev else 'unknown'}")
    return True


def cmd_list(models):
    ok = [(m, repo_id(m)) for m in models]
    fetchable = [(m, r) for m, r in ok if r]
    print(f"  {len(fetchable)} of {len(models)} models have a specific repo recorded\n")
    for m, r in sorted(fetchable, key=lambda x: (x[0]["category"], x[0]["name"])):
        flag = {"no": "⛔", "conditional": "⚠️ ", "yes": "  "}.get(m["commercial_use"], "  ")
        print(f"  {flag} {m['id']:<28}{r}")
    missing = [m for m, r in ok if not r]
    if missing:
        print(f"\n  {len(missing)} need a repo_id added to data/ before they can be fetched:")
        print("   " + ", ".join(m["id"] for m in missing))


def cmd_status(models):
    man = load_manifest()
    if not man["models"]:
        print("  Nothing downloaded yet.  python3 scripts/fetch.py --list")
        return
    total = sum(v.get("size_gb") or 0 for v in man["models"].values())
    print(f"  {len(man['models'])} models · {total:.1f}GB in models/\n")
    for mid, v in sorted(man["models"].items()):
        cu = {"no": "⛔ non-commercial", "conditional": "⚠️  conditional"}.get(
            v.get("commercial_use"), "")
        print(f"  {mid:<28}{v.get('size_gb', 0):>7.2f}GB  {v.get('license') or '—':<22}{cu}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--yes", action="store_true", help="skip prompts (still refuses nothing)")
    ap.add_argument("--include", nargs="*", help="only these file patterns, e.g. '*.safetensors'")
    a = ap.parse_args()

    models, _ = load()
    index = {m["id"]: m for m in models}

    if a.list:
        return cmd_list(models) or 0
    if a.status:
        return cmd_status(models) or 0
    if not a.ids:
        ap.print_help()
        return 1

    man = load_manifest()
    done = 0
    for mid in a.ids:
        if mid not in index:
            print(f"  ✕ unknown model id: {mid}")
            continue
        if fetch_one(index[mid], a, man):
            done += 1
    print(f"\n  {done}/{len(a.ids)} fetched · models/manifest.json updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
