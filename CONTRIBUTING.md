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

**Record `params_b` when the figure is public.** It is the numeric total parameter count in
billions, and it is what lets `scripts/check_env.py` estimate VRAM for readers whose hardware
you know nothing about. For MoE models use the **total**, not the active count, and note the
active count in `params_note`.

**Do not invent `vram_min_gb`.** That field is for figures someone actually published. If you
only have a parameter count, fill `params_b` and leave `vram_min_gb` null — the checker will
estimate and label it as an estimate.

**Improving `runs_on` is high-value.** Most entries say only `gpu`, which forces the checker
to report "support not confirmed" on Apple Silicon and ROCm machines. Adding
`apple-silicon` where you have verified it removes real uncertainty for readers.

**Get `inputs` / `outputs` right.** These two fields decide whether models may be connected.
An error here produces invalid pipelines in the composition editor.

**Check `commercial_use` before writing it.** If it is `conditional`, `license_note` must say
what the condition is.

## Please don't

- Edit `README.md` or `dist/index.json` directly — they are generated
- Add benchmark numbers without a source
- Present vendor-reported figures as independent — mark them in the entry's `note`
