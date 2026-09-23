#!/usr/bin/env python3
"""Validate the catalog against the rules in SCHEMA.md."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import (load, CATEGORIES, TYPES, OPENNESS, COMMERCIAL,
                     REQUIRED, NULLABLE_REQUIRED, OPTIONAL_ENUMS)


def main():
    models, files = load()
    errs, warns = [], []
    seen = {}

    for m in models:
        mid = m.get("id", "(missing id)")
        where = f'{m.get("_file")}:{mid}'

        for k in REQUIRED:
            if k not in m:
                errs.append(f"{where} — missing required key: {k}")
                continue
            if k in NULLABLE_REQUIRED:
                continue          # key required, value may be null (reported as a warning)
            v = m.get(k)
            if v is None or (isinstance(v, (list, str)) and len(v) == 0):
                errs.append(f"{where} — required field is empty: {k}")

        if mid in seen:
            errs.append(f"{where} — duplicate id (already in {seen[mid]})")
        seen[mid] = m.get("_file")

        if m.get("category") not in CATEGORIES:
            errs.append(f'{where} — unknown category: {m.get("category")}')
        if m.get("openness") not in OPENNESS:
            errs.append(f'{where} — openness must be one of {sorted(OPENNESS)}')
        if str(m.get("commercial_use")) not in COMMERCIAL:
            errs.append(f'{where} — commercial_use must be one of {sorted(COMMERCIAL)}')
        for k, allowed in OPTIONAL_ENUMS.items():
            if k in m and m[k] is not None and str(m[k]) not in allowed:
                errs.append(f"{where} — {k} must be one of {sorted(allowed)}")
        for side in ("inputs", "outputs"):
            for t in (m.get(side) or []):
                if t not in TYPES:
                    errs.append(f"{where} — unknown {side} type: {t}")

        # Warnings: entries stay usable but lose value without these
        if not m.get("license"):
            warns.append(f"{where} — license unverified")
        links = m.get("links") or {}
        if not links.get("huggingface") and not links.get("github"):
            warns.append(f"{where} — no download path (huggingface/github)")
        if m.get("commercial_use") == "conditional" and not m.get("license_note"):
            warns.append(f"{where} — commercial_use is conditional but license_note is empty")

    print(f"{len(files)} files · {len(models)} models")
    for e in errs:  print("  ERROR  " + e)
    for w in warns: print("  warn   " + w)
    print(f"\n{len(errs)} errors · {len(warns)} warnings")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
