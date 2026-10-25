"""Generates every plate in the profile system."""
import os
import ds as D
from ds import T, M, TW

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ds")
W = 1000
MARGIN = 48

files = {}


def emit(name, svg):
    files[name] = svg


# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
def cover():
    H = 480
    b = [D.plate(W, H), f'<g clip-path="url(#clip)">{D.grid(W, H)}</g>']
    for cx, sy in [(13, 1), (W - 13, 1)]:
        b.append(f'<path d="M{cx + 9*sy} 13 L{cx} 13 L{cx} 22" stroke="{D.INK3}" '
                 f'stroke-width="1" opacity="0.35" fill="none"/>')

    b.append(M("SOFTWARE ENGINEER — PORTFOLIO INDEX", MARGIN, 44, 9.5, D.INK3, 2.3))
    b.append(M("ED. 2026  /  DHAKA, BANGLADESH  ·  23.8103°N 90.4125°E",
               W - MARGIN, 44, 9.5, D.INK3, 2.3, anchor="end"))
    b.append(D.rule(MARGIN, 58, W - MARGIN, 58))

    b.append(f'<rect x="{MARGIN}" y="112" width="7" height="7" fill="{D.ACC}"/>')
    b.append(M("SHAFIUR RAHMAN", MARGIN + 17, 120, 12, D.ACC, 4.2))

    size, track = 240, -8
    b.append(T("SHAFIM", MARGIN, 330, size, "url(#inkG)", track))
    wm = TW("SHAFIM", size, track)
    b.append(f'<rect x="{MARGIN+wm+22}" y="306" width="24" height="24" fill="{D.ACC}">'
             f'<animate attributeName="opacity" values="1;1;0.12;1" dur="4.6s" '
             f'repeatCount="indefinite" keyTimes="0;0.87;0.94;1"/></rect>')

    b.append(D.rule(MARGIN, 364, MARGIN + wm + 46, 364, D.HAIR2))
    b.append(f'<line x1="{MARGIN}" y1="364" x2="{MARGIN+56}" y2="364" stroke="{D.ACC}" '
             f'stroke-width="2"/>')
    b.append(M("FULL-STACK ENGINEERING · EMBEDDED IOT · APPLIED MACHINE LEARNING",
               MARGIN, 394, 11.5, D.INK2, 2.6))
    b.append(M("B.SC. SOFTWARE ENGINEERING — DAFFODIL INTERNATIONAL UNIVERSITY  /  "
               "CORTEX CREW · LEAD SOFTWARE & ROBOTICS ARCHITECT",
               MARGIN, 416, 9, D.INK3, 1.9))

    b.append(D.rule(MARGIN, 436, W - MARGIN, 436))
    x = MARGIN
    stats = [("32", "REPOSITORIES"), ("06", "AWARDS"), ("2024", "ACTIVE SINCE")]
    for i, (num, lab) in enumerate(stats):
        nw = TW(num, 19)
        b.append(T(num, x, 462, 19, D.INK, -0.3))
        lx = x + nw + 9
        b.append(M(lab, lx, 461, 8.5, D.INK3, 1.7))
        x = lx + len(lab) * 6.8 + 34
        if i < len(stats) - 1:
            b.append(D.rule(x - 17, 447, x - 17, 469, D.HAIR))

    px = W - MARGIN - 200
    b.append(f'<circle cx="{px+6}" cy="457" r="3.2" fill="{D.ACC}"/>'
             f'<circle cx="{px+6}" cy="457" r="3.2" fill="none" stroke="{D.ACC}" '
             f'stroke-width="1"><animate attributeName="r" values="3.2;15" dur="2.8s" '
             f'repeatCount="indefinite"/><animate attributeName="opacity" values="0.65;0" '
             f'dur="2.8s" repeatCount="indefinite"/></circle>')
    b.append(M("OPEN TO COLLABORATE", px + 20, 461, 9.5, D.INK2, 2.1))

    b.append(f'<g clip-path="url(#clip)"><g><rect x="0" y="-170" width="{W}" height="170" '
             f'fill="url(#sweep)"/><animateTransform attributeName="transform" '
             f'type="translate" from="0 0" to="0 {H+170}" dur="13s" '
             f'repeatCount="indefinite"/></g></g>')

    defs = (D.ink_grad() +
            f'<clipPath id="clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15"/></clipPath>'
            f'<linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{D.ACC}" stop-opacity="0"/>'
            f'<stop offset="70%" stop-color="{D.ACC}" stop-opacity="0.055"/>'
            f'<stop offset="100%" stop-color="{D.ACC}" stop-opacity="0"/></linearGradient>')
    emit("cover.svg", D.svg(W, H, "".join(b), defs))


# ══════════════════════════════════════════════════════════════════════════════
# LINK CHIPS  (nav + contact) — clickable when wrapped in <a>
# ══════════════════════════════════════════════════════════════════════════════
def arrow(x, y, s=7.0, color=None, w=1.25):
    """Up-right arrow with (x, y) at the tip's baseline corner."""
    color = color or D.ACC
    return (f'<path d="M{x-s} {y} L{x} {y-s} M{x-s*0.45} {y-s} L{x} {y-s} '
            f'L{x} {y-s*0.45}" stroke="{color}" stroke-width="{w}" fill="none" '
            f'stroke-linecap="square"/>')


def chip(num, label, cid, is_arrow=False):
    cw, ch = 172, 50
    x0, y0, iw, ih = 7, 7, 158, 36
    nsize, ntrack = 8.6, 1.4
    lsize, ltrack = 10.2, 2.1
    nw = 9.0 if is_arrow else D.MOW(num, nsize, ntrack)
    lw = D.MOW(label, lsize, ltrack)
    gap = 14
    group = nw + gap + lw
    start = x0 + (iw - group) / 2.0
    b = [f'<rect x="{x0+0.5}" y="{y0+0.5}" width="{iw-1}" height="{ih-1}" rx="4" '
         f'fill="{D.PANEL}" stroke="{D.HAIR}" stroke-width="1"/>']
    if is_arrow:
        b.append(arrow(start + 8, y0 + 26, 7.4))
    else:
        b.append(D.MO(num, start, y0 + 23, nsize, D.ACC, ntrack))
    b.append(D.MO(label, start + nw + gap, y0 + 23, lsize, D.INK2, ltrack))
    emit(cid, D.svg(cw, ch, "".join(b)))


NAV = [("01", "PROFILE"), ("02", "STACK"), ("03", "WORK"),
       ("04", "AWARDS"), ("05", "STATS"), ("06", "CONTACT")]
for i, (n, l) in enumerate(NAV):
    chip(n, l, f"nav-{i+1:02d}.svg")

CONTACT = ["EMAIL", "PORTFOLIO", "LINKEDIN", "GITHUB", "X", "YOUTUBE"]
for i, l in enumerate(CONTACT):
    chip("", l, f"cta-{i+1:02d}.svg", is_arrow=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION HEADERS
# ══════════════════════════════════════════════════════════════════════════════
def header(num, title, sub, idx):
    H = 100
    b = [D.plate(W, H, rx=12),
         f'<g clip-path="url(#hc)">{D.grid(W, H, 62.5, 50)}</g>']
    b.append(D.rule(MARGIN, 34, MARGIN, 64, D.HAIR2))
    b.append(D.rule(MARGIN + 40, 34, MARGIN + 40, 64, D.HAIR2))
    b.append(T(num, MARGIN + 11, 56, 21, D.ACC, 0.4))
    b.append(T(title, MARGIN + 62, 56, 29, D.INK, -0.6))
    b.append(M(sub, MARGIN + 62, 78, 9, D.INK3, 2.2))
    b.append(M(f"SEC. {num} / 06", W - MARGIN, 56, 9, D.INK3, 2.0, anchor="end"))
    b.append(f'<line x1="{MARGIN}" y1="90" x2="{MARGIN+64}" y2="90" stroke="{D.ACC}" '
             f'stroke-width="2"/>')
    defs = (f'<clipPath id="hc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="11"/>'
            f'</clipPath>')
    emit(f"head-{idx:02d}.svg", D.svg(W, H, "".join(b), defs))


HEADERS = [
    ("01", "PROFILE", "SYSTEM CORE — IDENTITY, DISCIPLINE, INTENT"),
    ("02", "STACK", "TECH MATRIX — LAYERS, TOOLS, DEPTH"),
    ("03", "WORK", "SELECTED BUILDS — SHIPPED & AWARDED"),
    ("04", "AWARDS", "HALL OF FAME — VERIFIED RECOGNITION"),
    ("05", "STATS", "TELEMETRY — LIVE GITHUB SIGNAL"),
    ("06", "CONTACT", "UPLINK — OPEN CHANNELS"),
]
for i, (n, t, s) in enumerate(HEADERS):
    header(n, t, s, i + 1)


# ══════════════════════════════════════════════════════════════════════════════
# SPEC SHEET
# ══════════════════════════════════════════════════════════════════════════════
def spec():
    rows = [
        ("NAME", "SHAFIUR RAHMAN SHAFIM", False),
        ("ROLE", "SOFTWARE ENGINEER — FULL-STACK & IOT SYSTEMS", False),
        ("BASE", "DHAKA, BANGLADESH  ·  23.8103°N  90.4125°E", False),
        ("STUDYING", "B.SC. SOFTWARE ENGINEERING — DAFFODIL INTERNATIONAL UNIVERSITY", False),
        ("TEAM", "CORTEX CREW — LEAD SOFTWARE & ROBOTICS ARCHITECT", False),
        ("STATUS", "OPEN TO INTERNSHIPS, RESEARCH & COLLABORATION", True),
    ]
    top, rh = 26, 46
    H = top + rh * len(rows) + 16
    b = [D.plate(W, H)]
    for i, (lab, val, hot) in enumerate(rows):
        y = top + i * rh
        b.append(M(lab, MARGIN, y + 27, 9, D.INK3, 2.1))
        b.append(M(val, 232, y + 27, 11.2, D.ACC if hot else D.INK, 0.9))
        b.append(M(f"{i+1:02d}", W - MARGIN, y + 27, 8.5, D.INK3, 1.3, anchor="end"))
        if i:
            b.append(D.rule(MARGIN, y, W - MARGIN, y))
    b.append(D.rule(MARGIN, top + rh * len(rows), W - MARGIN, top + rh * len(rows)))
    emit("spec.svg", D.svg(W, H, "".join(b)))


spec()


# ══════════════════════════════════════════════════════════════════════════════
# STACK MATRIX
# ══════════════════════════════════════════════════════════════════════════════
def stack():
    rows = [
        ("L01", "FRONTEND", 20, "REACT · NEXT.JS · TYPESCRIPT · TAILWIND · BOOTSTRAP"),
        ("L02", "BACKEND", 18, "NODE.JS · EXPRESS · PYTHON · JAVA · PHP · C / C++"),
        ("L03", "DATA & INFRA", 16, "MONGODB · POSTGRESQL · MYSQL · DOCKER · LINUX · AWS"),
        ("L04", "HARDWARE", 15, "ESP32 · ARDUINO C++ · RASPBERRY PI · MQTT · SENSORS"),
        ("L05", "AI / ML", 13, "TENSORFLOW · OPENCV · SCIKIT-LEARN · FASTAPI · RAG"),
    ]
    top, rh = 26, 58
    H = top + rh * len(rows) + 14
    b = [D.plate(W, H), f'<g clip-path="url(#clip2)">{D.grid(W, H, 62.5, 58)}</g>']

    b.append(M("LAYER", MARGIN, 18, 8, D.INK3, 1.8))
    b.append(M("DEPTH", 300, 18, 8, D.INK3, 1.8))
    b.append(M("TOOLING", 528, 18, 8, D.INK3, 1.8))

    for i, (code, name, level, tools) in enumerate(rows):
        y = top + i * rh
        cy = y + rh / 2
        b.append(M(code, MARGIN, cy + 3.4, 8.5, D.ACC, 1.3))
        b.append(T(name, 96, cy + 6, 16, D.INK, -0.2, w=500))
        # segmented meter
        for s in range(20):
            sx = 300 + s * 10
            on = s < level
            b.append(f'<rect x="{sx}" y="{cy-4}" width="7" height="8" rx="1" '
                     f'fill="{D.ACC if on else D.HAIR2}" opacity="{1 if on else 0.85}"/>')
        b.append(M(tools, 528, cy + 3.4, 9.5, D.INK2, 0.7))
        if i:
            b.append(D.rule(MARGIN, y, W - MARGIN, y))

    b.append(D.rule(MARGIN, top + rh * len(rows), W - MARGIN, top + rh * len(rows)))
    defs = (f'<clipPath id="clip2"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15"/>'
            f'</clipPath>')
    emit("stack.svg", D.svg(W, H, "".join(b), defs))


stack()


# ══════════════════════════════════════════════════════════════════════════════
# PROJECT CARDS
# ══════════════════════════════════════════════════════════════════════════════
def glyph(kind, cx, cy):
    """Small technical glyph, unique per project."""
    if kind == "radar":
        g = [f'<circle cx="{cx}" cy="{cy}" r="34" stroke="{D.HAIR2}" stroke-width="1"/>',
             f'<circle cx="{cx}" cy="{cy}" r="21" stroke="{D.HAIR2}" stroke-width="1"/>',
             f'<circle cx="{cx}" cy="{cy}" r="8" stroke="{D.HAIR2}" stroke-width="1"/>',
             f'<circle cx="{cx}" cy="{cy}" r="2.4" fill="{D.ACC}"/>',
             f'<path d="M{cx-38} {cy} H{cx+38} M{cx} {cy-38} V{cy+38}" stroke="{D.HAIR2}" '
             f'stroke-width="1" opacity="0.6"/>']
        g.append(f'<g style="transform-origin:{cx}px {cy}px">'
                 f'<path d="M{cx} {cy} L{cx+34} {cy-10} A34 34 0 0 0 {cx+24} {cy-24} Z" '
                 f'fill="{D.ACC}" opacity="0.28"/>'
                 f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
                 f'to="360 {cx} {cy}" dur="7s" repeatCount="indefinite"/></g>')
        return "".join(g)
    if kind == "ecg":
        pts = [(cx - 40, cy), (cx - 22, cy), (cx - 16, cy - 20), (cx - 10, cy + 22),
               (cx - 2, cy - 30), (cx + 6, cy + 14), (cx + 14, cy), (cx + 40, cy)]
        d = "M" + " L".join(f"{x} {y}" for x, y in pts)
        return (f'<path d="{d}" stroke="{D.HAIR2}" stroke-width="1.4" fill="none"/>'
                f'<path d="{d}" stroke="{D.ACC}" stroke-width="2" fill="none" '
                f'stroke-dasharray="46 200" stroke-linecap="round">'
                f'<animate attributeName="stroke-dashoffset" from="246" to="-46" dur="3.4s" '
                f'repeatCount="indefinite"/></path>'
                f'<circle cx="{cx+40}" cy="{cy}" r="2.4" fill="{D.ACC}"/>')
    if kind == "mesh":
        import math
        g = []
        n = 7
        pos = []
        for i in range(n):
            a = -math.pi / 2 + i * 2 * math.pi / n
            r = 30 if i % 2 == 0 else 18
            pos.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        for i in range(n):
            for j in range(i + 1, n):
                g.append(f'<line x1="{pos[i][0]:.1f}" y1="{pos[i][1]:.1f}" x2="{pos[j][0]:.1f}" '
                         f'y2="{pos[j][1]:.1f}" stroke="{D.HAIR2}" stroke-width="0.7" '
                         f'opacity="0.75"/>')
        for i, (px, py) in enumerate(pos):
            g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{3 if i==0 else 2.2}" '
                     f'fill="{D.ACC if i==0 else D.INK3}"/>')
            if i == 0:
                g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.2" fill="none" '
                         f'stroke="{D.ACC}" stroke-width="1">'
                         f'<animate attributeName="r" values="3;14" dur="2.4s" '
                         f'repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="0.7;0" dur="2.4s" '
                         f'repeatCount="indefinite"/></circle>')
        return "".join(g)
    if kind == "cube":
        s = 26
        top = f"{cx} {cy-s} {cx+s} {cy-s*0.5} {cx} {cy} {cx-s} {cy-s*0.5}"
        left = f"{cx-s} {cy-s*0.5} {cx} {cy} {cx} {cy+s} {cx-s} {cy+s*0.5}"
        right = f"{cx} {cy} {cx+s} {cy-s*0.5} {cx+s} {cy+s*0.5} {cx} {cy+s}"
        return (f'<polygon points="{top}" fill="none" stroke="{D.HAIR2}" stroke-width="1"/>'
                f'<polygon points="{left}" fill="none" stroke="{D.HAIR2}" stroke-width="1"/>'
                f'<polygon points="{right}" fill="none" stroke="{D.HAIR2}" stroke-width="1"/>'
                f'<polygon points="{top}" fill="{D.ACC}" opacity="0.22">'
                f'<animate attributeName="opacity" values="0.1;0.34;0.1" dur="5s" '
                f'repeatCount="indefinite"/></polygon>'
                f'<circle cx="{cx}" cy="{cy}" r="2.4" fill="{D.ACC}"/>')
    return ""


CARDS = [
    dict(num="01", kicker="AGRITECH / ML", title="BD-KRISHIBID", glyph="radar",
         sub="AI CROP DIAGNOSTICS PLATFORM",
         desc=["Computer-vision plant pathology, yield prediction and live",
               "commodity pricing for farmers across Bangladesh."],
         tags=["REACT", "NODE", "MONGODB", "PYTHON", "OPENCV"], note="FINALIST · DATA SCIENCE SUMMIT"),
    dict(num="02", kicker="HEALTH / CV", title="NIIRO 2.0", glyph="ecg",
         sub="NON-INVASIVE MEDICAL SCREENING",
         desc=["Deep-learning screening pipeline that turns clinical images",
               "into early-warning diagnostic reports."],
         tags=["TENSORFLOW", "FASTAPI", "REACT", "OPENCV"], note="1ST RUNNER-UP · IEEE ICADHI"),
    dict(num="03", kicker="IOT / FIRMWARE", title="SMART HOME IOT", glyph="mesh",
         sub="DISTRIBUTED TELEMETRY MESH",
         desc=["ESP32 sensor mesh with MQTT transport, low-latency edge",
               "automation and a remote control dashboard."],
         tags=["ESP32", "ARDUINO C++", "MQTT", "NODE"], note="HARDWARE · EDGE · CLOUD"),
    dict(num="04", kicker="WEBGL / PRODUCT", title="NEXORA 3D OS", glyph="cube",
         sub="BROWSER OPERATING ENVIRONMENT",
         desc=["Hardware-accelerated WebGL workspace with a glassmorphic",
               "window manager, live at shafim.vercel.app."],
         tags=["THREE.JS", "REACT", "TYPESCRIPT", "VERCEL"], note="LIVE · PRODUCTION"),
]


def card(c):
    CW, CH = 480, 306
    b = [D.plate(CW, CH, rx=12, fill=D.PANEL)]
    b.append(f'<g clip-path="url(#cc)">{D.grid(CW, CH, 60, 51, opacity=0.028)}</g>')
    b.append(glyph(c["glyph"], 400, 78))
    b.append(M(f'{c["num"]} / {c["kicker"]}', 28, 40, 8.5, D.ACC, 2.0))
    b.append(T(c["title"], 28, 106, 25, D.INK, -0.5))
    b.append(M(c["sub"], 28, 128, 8.5, D.INK3, 2.0))
    for i, line in enumerate(c["desc"]):
        b.append(M(line, 28, 166 + i * 18, 10, D.INK2, 0.4))
    b.append(D.rule(28, 216, CW - 28, 216))
    tx = 28
    for t in c["tags"]:
        tw = len(t) * 5.6 + len(t) * 1.2 + 16
        b.append(f'<rect x="{tx}" y="234" width="{tw:.0f}" height="20" rx="3" '
                 f'fill="{D.PANEL2}" stroke="{D.HAIR}" stroke-width="1"/>')
        b.append(M(t, tx + 8, 248, 7.6, D.INK2, 1.2))
        tx += tw + 6
    b.append(M(c["note"], 28, 282, 8, D.INK3, 1.6))
    b.append(M("OPEN", CW - 46, 282, 8, D.ACC, 1.6, anchor="end"))
    b.append(arrow(CW - 30, 284, 6.4))
    defs = (f'<clipPath id="cc"><rect x="1" y="1" width="{CW-2}" height="{CH-2}" rx="11"/>'
            f'</clipPath>')
    return D.svg(CW, CH, "".join(b), defs)


for i, c in enumerate(CARDS):
    emit(f"card-{i+1:02d}.svg", card(c))


# ══════════════════════════════════════════════════════════════════════════════
# WORK INDEX LEDGER
# ══════════════════════════════════════════════════════════════════════════════
def work_index():
    rows = [
        ("01", "ECHOES OF THE LAST STAR", "THREE.JS · PROCEDURAL AUDIO", "3D · NARRATIVE GAME"),
        ("02", "NEON ARENA", "THREE.JS · BLOOM · WEB AUDIO", "3D · ARCADE SHOOTER"),
        ("03", "MY CLIMATE STORY", "JAVASCRIPT · NASA OPEN DATA", "DATA · EARTH SCIENCE"),
        ("04", "BANGLA DIALECT VOICE RAG", "TYPESCRIPT · RAG · EMBEDDINGS", "AI · LOW-RESOURCE SPEECH"),
        ("05", "GITVIZ", "TYPESCRIPT · GITHUB API", "DEVTOOLS · VISUALISATION"),
        ("06", "DIGITAL VOTING SYSTEM", "C · FILE-BASED STORAGE", "SYSTEMS · C"),
    ]
    top, rh = 50, 46
    H = top + rh * len(rows) + 16
    b = [D.plate(W, H)]
    for x, lab in [(MARGIN, "NO."), (100, "PROJECT"), (404, "STACK"), (716, "DOMAIN")]:
        b.append(M(lab, x, 32, 8, D.INK3, 1.9))
    b.append(D.rule(MARGIN, 42, W - MARGIN, 42, D.HAIR2))

    for i, (no, proj, stack, dom) in enumerate(rows):
        y = top + i * rh
        cy = y + rh / 2 + 5
        b.append(M(no, MARGIN, cy, 8.5, D.ACC, 1.3))
        b.append(T(proj, 100, cy + 1, 15, D.INK, -0.2, w=500))
        b.append(M(stack, 404, cy, 8.4, D.INK2, 0.9))
        b.append(M(dom, 716, cy, 8.4, D.INK3, 1.1))
        if i:
            b.append(D.rule(MARGIN, y, W - MARGIN, y))
    b.append(D.rule(MARGIN, top + rh * len(rows), W - MARGIN, top + rh * len(rows)))
    emit("work-index.svg", D.svg(W, H, "".join(b)))


work_index()


# ══════════════════════════════════════════════════════════════════════════════
# AWARDS LEDGER
# ══════════════════════════════════════════════════════════════════════════════
def awards():
    rows = [
        ("2026", "CHAMPION", "CSAD — CYBER SECURITY CENTER, DIU", "DREAKTARACE3", "01"),
        ("2026", "FIRST RUNNER-UP", "IEEE ICADHI — INTERNATIONAL CONFERENCE", "NIIRO 2.0", "02"),
        ("2026", "FINALIST", "5TH DATA SCIENCE SUMMIT — DIU SWE", "BD-KRISHIBID", "03"),
        ("2026", "FINALIST", "UFTB ROBOTICS FUSION 1.0 — NATIONAL", "CORTEX CREW", "04"),
    ]
    top, rh = 52, 56
    H = top + rh * len(rows) + 18
    b = [D.plate(W, H)]
    for x, lab in [(MARGIN, "YEAR"), (128, "NO."), (196, "HONOR"), (536, "VENUE"),
                   (830, "PROJECT")]:
        b.append(M(lab, x, 34, 8, D.INK3, 1.9))
    b.append(D.rule(MARGIN, 44, W - MARGIN, 44, D.HAIR2))

    for i, (yr, honor, venue, proj, no) in enumerate(rows):
        y = top + i * rh
        cy = y + rh / 2 + 5
        b.append(M(yr, MARGIN, cy, 10, D.INK3, 1.4))
        b.append(M(no, 128, cy, 8.5, D.ACC, 1.3))
        b.append(T(honor, 196, cy + 1, 16.5, D.INK, -0.2, w=500))
        b.append(M(venue, 536, cy, 8.6, D.INK2, 0.9))
        b.append(M(proj, 830, cy, 8.6, D.ACC, 1.1))
        if i:
            b.append(D.rule(MARGIN, y, W - MARGIN, y))

    b.append(D.rule(MARGIN, top + rh * len(rows), W - MARGIN, top + rh * len(rows)))
    emit("awards.svg", D.svg(W, H, "".join(b)))


awards()


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
def footer():
    H = 268
    b = [D.plate(W, H), f'<g clip-path="url(#fc)">{D.grid(W, H, 62.5, 52)}</g>']
    b.append(M("END OF DOCUMENT", MARGIN, 40, 8.5, D.INK3, 2.2))
    b.append(M("06 / 06", W - MARGIN, 40, 8.5, D.INK3, 2.2, anchor="end"))
    b.append(D.rule(MARGIN, 52, W - MARGIN, 52))

    b.append(T("LET'S BUILD", MARGIN, 138, 76, "url(#fg)", -2.4))
    b.append(T("SOMETHING REAL", MARGIN, 200, 76, D.ACC, -2.4))

    b.append(D.rule(MARGIN, 226, W - MARGIN, 226))
    b.append(M("SHAFIUR RAHMAN SHAFIM  ·  DHAKA, BANGLADESH  ·  ENGINEERED IN THE OPEN",
               MARGIN, 250, 8.6, D.INK3, 1.8))
    b.append(M("© 2026", W - MARGIN, 250, 8.6, D.INK3, 1.8, anchor="end"))
    defs = (D.ink_grad("fg") +
            f'<clipPath id="fc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15"/>'
            f'</clipPath>')
    emit("footer.svg", D.svg(W, H, "".join(b), defs))


footer()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, s in files.items():
        p = os.path.join(OUT, name)
        open(p, "w", encoding="utf-8").write(s)
        total += len(s)
        print(f"{name:16s} {len(s):7d}")
    print(f"{'TOTAL':16s} {total:7d}  ({len(files)} files)")
