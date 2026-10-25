# build

The source of every plate in `assets/ds/`. Nothing here is imported by the
README at runtime — it exists so the artwork can be regenerated, edited, and
kept perfectly consistent.

## Files

| File | Role |
|---|---|
| `ds.py` | Design tokens (palette, type scale, hairlines) and SVG primitives |
| `type_engine.py` | Instantiates the variable fonts and converts text to outline paths |
| `gen_plates.py` | Cover, nav/contact chips, section headers, spec sheet, stack matrix, project cards, ledgers, footer |
| `gen_telemetry.py` | Fetches live GitHub data and renders `telemetry.svg` |
| `v3.py` | Pinhole camera, projection, depth sorting, shaded boxes for the 3D plates |
| `preview_full.py` | Renders `README.md` to HTML/PNG for visual QA |
| `shot.py` | Screenshots individual plates at a given scale |

## Regenerating

```bash
pip install fonttools markdown

python build/gen_plates.py                              # all static plates
python build/gen_telemetry.py --login Shafiur0          # needs GITHUB_TOKEN
```

`gen_telemetry.py` is also run daily by `.github/workflows/telemetry.yml`, which
commits the refreshed plate back to `main`.

## Design system

- **Palette** — obsidian `#0A0A0C`, panel `#101014`, hairline `#26262D`,
  bone `#F2F1EC`, vermilion `#FF4B1F` as the single accent.
- **Grid** — 1000 × *n* canvas, 48px outer margin, 62.5px vertical rhythm.
- **Type** — Space Grotesk for display (outlined), JetBrains Mono for micro-labels.
- **Plates** — every asset is a self-contained dark card with a hairline border,
  so it reads identically on GitHub's light and dark themes with no theme sniffing.
- **3D** — the contribution city and the hero layer stack are real projected geometry
  (pinhole camera, depth-sorted, atmospheric fog), not flat illustrations.
- **Motion** — SMIL/CSS animation only: sweep, pulse, radar rotation, ECG dash, layer float.
  No scripts, no third-party rendering services.
