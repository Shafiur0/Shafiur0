# Fonts

Both typefaces are bundled here so the plates in `assets/ds/` can be rendered
reproducibly — the generator converts every display string to SVG outlines, so
the output is identical on every machine and never depends on what the viewer
has installed.

| File | Family | License |
|---|---|---|
| `SpaceGrotesk.ttf` | [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) — variable, weight axis | SIL Open Font License 1.1 |
| `JetBrainsMono.ttf` | [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) — variable, weight axis | SIL Open Font License 1.1 |

Both are distributed under the SIL Open Font License, Version 1.1, which permits
bundling and embedding. Full license text: <https://openfontlicense.org>.

Small monospace labels that stay as live `<text>` in the SVGs fall back to the
viewer's system monospace stack, which is metrically close enough at those sizes.
