"""Design tokens + SVG primitives for the Shafim profile plates."""
from type_engine import Face

# ── palette ────────────────────────────────────────────────────────────────────
BG      = "#0A0A0C"
PANEL   = "#101014"
PANEL2  = "#17171D"
HAIR    = "#2A2A32"
HAIR2   = "#3A3A44"
INK     = "#F2F1EC"
INK2    = "#9C9CA6"
INK3    = "#5C5C67"
ACC     = "#FF4B1F"
ACC_DIM = "#7A2410"

MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# ── faces ──────────────────────────────────────────────────────────────────────
_disp = {}
_mono = {}


def disp(weight=700):
    if weight not in _disp:
        _disp[weight] = Face("SpaceGrotesk.ttf", weight)
    return _disp[weight]


def mono(weight=500):
    if weight not in _mono:
        _mono[weight] = Face("JetBrainsMono.ttf", weight)
    return _mono[weight]


def MO(text, x, y, size=10, fill=INK3, tracking=1.6, anchor="start", weight=500):
    """Outlined monospace text (JetBrains Mono) — pixel-identical everywhere."""
    f = mono(weight)
    if anchor == "middle":
        d = f.path_center(text, x, y, size, tracking)
    elif anchor == "end":
        d = f.path_right(text, x, y, size, tracking)
    else:
        d = f.path(text, x, y, size, tracking)
    return f'<path d="{d}" fill="{fill}"/>'


def MOW(text, size, tracking=1.6, weight=500):
    return mono(weight).width(text, size, tracking)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def T(text, x, y, size, fill=INK, tracking=0.0, anchor="start", opacity=None, w=700):
    """Outlined display text."""
    f = disp(w)
    if anchor == "middle":
        d = f.path_center(text, x, y, size, tracking)
    elif anchor == "end":
        d = f.path_right(text, x, y, size, tracking)
    else:
        d = f.path(text, x, y, size, tracking)
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<path d="{d}" fill="{fill}"{o}/>'


def TW(text, size, tracking=0.0, w=700):
    return disp(w).width(text, size, tracking)


def M(text, x, y, size=10, fill=INK3, tracking=2.0, anchor="start", opacity=None,
      weight=400, cls=""):
    """Monospace micro-label (stays as live text — crisper at small sizes)."""
    if anchor == "end":
        x = x + tracking
    o = f' opacity="{opacity}"' if opacity is not None else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{MONO}" font-size="{size}" '
            f'letter-spacing="{tracking}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{o}{c}>{esc(text)}</text>')


def svg(w, h, body, defs="", extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" fill="none" role="img"{extra}>'
            f'<defs>{defs}</defs>{body}</svg>')


def plate(w, h, rx=16, fill=BG, stroke=HAIR):
    return (f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>')


def rule(x1, y1, x2, y2, color=HAIR, width=1, opacity=None, dash=None):
    o = f' opacity="{opacity}"' if opacity is not None else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{width}"{o}{d}/>')


def grid(w, h, step_x=62.5, step_y=55, color="#FFFFFF", opacity=0.032, inset=0):
    out = []
    x = step_x
    while x < w - inset:
        out.append(f'<line x1="{x}" y1="{inset}" x2="{x}" y2="{h-inset}" stroke="{color}" '
                   f'stroke-width="1" opacity="{opacity}"/>')
        x += step_x
    y = step_y
    while y < h - inset:
        out.append(f'<line x1="{inset}" y1="{y}" x2="{w-inset}" y2="{y}" stroke="{color}" '
                   f'stroke-width="1" opacity="{opacity}"/>')
        y += step_y
    return "".join(out)


def corner_marks(w, h, inset=22, length=11, color=INK3, opacity=0.45):
    o = []
    pts = [(inset, inset, 1, 1), (w - inset, inset, -1, 1),
           (inset, h - inset, 1, -1), (w - inset, h - inset, -1, -1)]
    for cx, cy, sx, sy in pts:
        o.append(f'<path d="M{cx + sx*length} {cy} L{cx} {cy} L{cx} {cy + sy*length}" '
                 f'stroke="{color}" stroke-width="1" opacity="{opacity}" fill="none"/>')
    return "".join(o)


def plate_defs(w, h, rx=15, gid="grainF"):
    """Shared <defs> for a plate: rounded clip + film-grain filter."""
    return (f'<filter id="{gid}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" '
            f'stitchTiles="stitch"/>'
            f'<feColorMatrix type="saturate" values="0"/></filter>'
            f'<clipPath id="plateClip"><rect x="1" y="1" width="{w-2}" height="{h-2}" '
            f'rx="{rx}"/></clipPath>')


def grain(w, h, opacity=0.05, gid="grainF"):
    """Fine film grain laid over a plate — reads as print texture, not noise."""
    return (f'<rect x="0" y="0" width="{w}" height="{h}" filter="url(#{gid})" '
            f'opacity="{opacity}" clip-path="url(#plateClip)" pointer-events="none"/>')


def ink_grad(gid="inkG"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="#FFFFFF"/>'
            f'<stop offset="55%" stop-color="{INK}"/>'
            f'<stop offset="100%" stop-color="#9E9EA8"/>'
            f'</linearGradient>')


def accent_grad(gid="accG"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0%" stop-color="#FF7A45"/>'
            f'<stop offset="100%" stop-color="{ACC}"/>'
            f'</linearGradient>')


def chip(w, h, x, y, label, num=None, rx=5, fill=PANEL, stroke=HAIR,
         label_color=INK2, num_color=ACC, size=10.5):
    """Small pill used for nav / contact links."""
    parts = [f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="{rx}" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>']
    cx = x + 16
    if num:
        parts.append(M(num, cx, y + h / 2 + 3.4, size=8.5, fill=num_color, tracking=1.4))
        cx += TW("00", 8.5) * 0 + 26
    parts.append(M(label, cx, y + h / 2 + 3.4, size=size, fill=label_color, tracking=1.8))
    return "".join(parts)
