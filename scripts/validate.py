#!/usr/bin/env python3
"""카탈로그 스키마 검증. SCHEMA.md 의 규칙을 강제한다."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import (load, CATEGORIES, TYPES, OPENNESS, COMMERCIAL,
                     REQUIRED, NULLABLE_REQUIRED)


def main():
    models, files = load()
    errs, warns = [], []
    seen = {}

    for m in models:
        mid = m.get("id","(id 없음)")
        where = f'{m.get("_file")}:{mid}'
        for k in REQUIRED:
            if k not in m:
                errs.append(f"{where} — 필수 키 없음: {k}")
                continue
            if k in NULLABLE_REQUIRED:
                continue            # 키는 있어야 하나 값은 null 허용 (경고로 처리)
            v = m.get(k)
            if v is None or (isinstance(v,(list,str)) and len(v)==0):
                errs.append(f"{where} — 필수 필드 비어 있음: {k}")
        if mid in seen:
            errs.append(f"{where} — ID 중복 (앞서 {seen[mid]} 에 있음)")
        seen[mid] = m.get("_file")

        if m.get("category") not in CATEGORIES:
            errs.append(f'{where} — 알 수 없는 category: {m.get("category")}')
        if m.get("openness") not in OPENNESS:
            errs.append(f'{where} — openness 는 {OPENNESS} 중 하나여야 함')
        if str(m.get("commercial_use")) not in COMMERCIAL:
            errs.append(f'{where} — commercial_use 는 {COMMERCIAL} 중 하나여야 함')
        for side in ("inputs","outputs"):
            for t in (m.get(side) or []):
                if t not in TYPES:
                    errs.append(f"{where} — 알 수 없는 {side} 타입: {t}")

        # 경고: 비어 있으면 카탈로그 가치가 떨어지는 항목
        if m.get("license") in (None,"null"):
            warns.append(f"{where} — license 미확인")
        if not m.get("links",{}).get("huggingface") and not m.get("links",{}).get("github"):
            warns.append(f"{where} — 다운로드 경로(hf/github) 없음")
        if m.get("commercial_use") == "conditional" and not m.get("license_note"):
            warns.append(f"{where} — commercial_use=conditional 인데 license_note 가 비어 있음")

    print(f"파일 {len(files)}개 · 모델 {len(models)}개")
    for e in errs:  print("  ERROR  " + e)
    for w in warns: print("  warn   " + w)
    print(f"\n오류 {len(errs)} · 경고 {len(warns)}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
