# 기여 안내

## 모델 추가

1. [`data/`](data/) 에서 카테고리에 맞는 YAML 파일을 연다
2. [`SCHEMA.md`](SCHEMA.md) 의 필드 정의를 따라 항목을 추가한다
3. 검증과 빌드를 돌린다

```bash
python3 scripts/validate.py   # 오류 0 이어야 한다
python3 scripts/build.py      # README.md · dist/index.json 재생성
```

4. 생성된 `README.md` 와 `dist/index.json` 을 함께 커밋한다

## 지켜야 할 것

**모르는 값은 `null` 로 둔다.** VRAM 요건이나 라이선스를 추측해서 적으면
사용자가 실제로 손해를 본다. 검증기가 경고로 알려주며, 경고가 있어도 병합은 가능하다.

**`sources` 에 근거 링크를 넣는다.** 벤더 발표인지 독립 벤치마크인지 구분할 수 있어야 한다.

**`inputs` / `outputs` 를 정확히 적는다.** 이 두 필드로 모델 간 연결 가능 여부가
판정되므로, 틀리면 조합 편집기에서 잘못된 파이프라인이 만들어진다.

**`commercial_use` 를 확인하고 적는다.** `conditional` 이면 `license_note` 에
무엇이 조건인지 반드시 쓴다.

## 하지 말아야 할 것

- `README.md` 와 `dist/index.json` 을 직접 수정하지 않는다 (생성물이다)
- 벤치마크 수치를 출처 없이 적지 않는다
- 벤더 자체 보고치는 `note` 에 그렇다고 표시한다
