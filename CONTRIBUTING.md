# Contributing

## Adding a model

1. Open the YAML file under [`data/`](data/) that matches the category
2. Add an entry following the field definitions in [`SCHEMA.md`](SCHEMA.md)
3. Validate and rebuild:

```bash
python3 scripts/validate.py   # must report 0 errors
python3 scripts/build.py      # regenerates README.md and dist/index.json
```

4. Commit the regenerated `README.md` and `dist/index.json` along with your data change

## Rules

**Leave unknown values as `null`.** A wrong VRAM requirement or license costs the reader real
time and money. The validator reports these as warnings; a warning does not block a merge.

**Put evidence in `sources`.** Readers need to tell a vendor announcement apart from an
independent benchmark.

**Get `inputs` / `outputs` right.** These two fields decide whether models may be connected.
An error here produces invalid pipelines in the composition editor.

**Check `commercial_use` before writing it.** If it is `conditional`, `license_note` must say
what the condition is.

## Please don't

- Edit `README.md` or `dist/index.json` directly — they are generated
- Add benchmark numbers without a source
- Present vendor-reported figures as independent — mark them in the entry's `note`
