"""Gives the generated snake SVG the same plate treatment as the hand-built ones.

snk emits a transparent SVG sized to its own viewBox. This injects a matching
obsidian background and hairline border so the animation reads as another plate
in the system rather than a pasted-in third-party graphic.
"""
import glob
import sys

BG = "#0A0A0C"
BORDER = "#2A2A32"
PLATE = (
    '<g id="snkplate">'
    '<rect x="-16" y="-32" width="880" height="192" rx="16" fill="' + BG + '"/>'
    '<rect x="-15.5" y="-31.5" width="879" height="191" rx="15.5" fill="none" '
    'stroke="' + BORDER + '"/>'
    '</g>'
)

files = sorted(glob.glob("dist/*.svg"))
if not files:
    print("no snake svg found in dist/", file=sys.stderr)
    sys.exit(1)

for path in files:
    s = open(path, encoding="utf-8").read()
    if 'id="snkplate"' in s:
        print(f"{path}: already patched")
        continue
    if "<desc>" not in s:
        print(f"{path}: unexpected structure, skipped", file=sys.stderr)
        continue
    s = s.replace("<desc>", PLATE + "<desc>", 1)
    open(path, "w", encoding="utf-8").write(s)
    print(f"{path}: plate injected ({len(s)} bytes)")
