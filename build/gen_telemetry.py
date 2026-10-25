"""Renders assets/ds/telemetry.svg from live GitHub data.

The contribution calendar is drawn as a perspective 3D city: every day is a
column, projected through a real pinhole camera, depth-sorted and fogged.

Usage:  python gen_telemetry.py [--token TOKEN] [--login USER]
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

import ds as D
import v3
from ds import M, MO, MOW, T

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ds")
W, H = 1000, 604
MARGIN = 48

API = "https://api.github.com"
GQL = "https://api.github.com/graphql"

LANG_RAMP = ["#FF4B1F", "#D9511E", "#B04520", "#87391F", "#5F2F1D", "#3A3A44", "#2A2A32"]
HEAT = ["#1B1B22", "#4A2318", "#7A2E17", "#B23A18", "#FF4B1F"]
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

QUERY = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    repositories(privacy:PUBLIC){totalCount}
    contributionsCollection{
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar{ totalContributions
        weeks{ contributionDays{ contributionCount date } } }
    }
  }
}
"""


def _req(url, token, data=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"bearer {token}",
                 "User-Agent": "shafim-profile-telemetry",
                 "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read())


def collect(login, token):
    g = _req(GQL, token, {"query": QUERY, "variables": {"login": login}})["data"]["user"]
    repos = _req(f"{API}/users/{login}/repos?per_page=100&sort=updated", token)
    stars = sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork"))
    lang_count = {}
    for r in repos:
        if r.get("fork"):
            continue
        lang = r.get("language")
        if lang:
            lang_count[lang] = lang_count.get(lang, 0) + 1
    cal = g["contributionsCollection"]["contributionCalendar"]
    weeks = [w["contributionDays"] for w in cal["weeks"]]

    days = sorted((d for w in weeks for d in w), key=lambda d: d["date"])
    streak = 0
    for d in reversed(days):
        if d["contributionCount"] > 0:
            streak += 1
        else:
            break

    return dict(
        contributions=cal["totalContributions"],
        commits=g["contributionsCollection"]["totalCommitContributions"],
        prs=g["contributionsCollection"]["totalPullRequestContributions"],
        stars=stars,
        repos=g["repositories"]["totalCount"],
        followers=g["followers"]["totalCount"],
        streak=streak,
        weeks=weeks,
        langs=sorted(lang_count.items(), key=lambda kv: -kv[1]),
        updated=datetime.now(timezone.utc).strftime("%d.%m.%Y"),
    )


# ── 3D contribution city ───────────────────────────────────────────────────────
def level(c):
    return 0 if c == 0 else 1 if c < 3 else 2 if c < 7 else 3 if c < 12 else 4


def city(weeks, rect, cell=0.88, max_h=15.0, yaw=-0.20, pitch=0.56, dist=170.0):
    nx, ny = len(weeks), max(len(w) for w in weeks)
    peak = max(1, max(d["contributionCount"] for w in weeks for d in w))
    x, y, w, h = rect

    probe = v3.Cam((nx / 2, ny / 2, max_h * 0.35), yaw, pitch, dist, 100.0, 0, 0)
    corners = [(cx, cy, cz) for cx in (0, nx) for cy in (0, ny)
               for cz in (0, max_h * 0.6)]
    pts = [probe.project(p) for p in corners]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    probe.focal = 100.0 * (w / (max(xs) - min(xs)))
    pts = [probe.project(p) for p in corners]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    probe.ox = x + w / 2 - (max(xs) + min(xs)) / 2
    probe.oy = y + h / 2 - (max(ys) + min(ys)) / 2
    cam = probe

    out = []
    # ground plane: week guides + front edge
    for i in range(0, nx + 1, 4):
        a, b = cam.project((i, 0, 0)), cam.project((i, ny, 0))
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" '
                   f'y2="{b[1]:.1f}" stroke="{D.HAIR2}" stroke-width="0.6" opacity="0.45"/>')
    for j in range(0, ny + 1, 2):
        a, b = cam.project((0, j, 0)), cam.project((nx, j, 0))
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" '
                   f'y2="{b[1]:.1f}" stroke="{D.HAIR2}" stroke-width="0.6" opacity="0.45"/>')

    faces = []
    for i, week in enumerate(weeks):
        for j, day in enumerate(week):
            c = day["contributionCount"]
            hgt = max_h * (c / peak) ** 0.62 if c else 0.0
            x0, y0 = i + (1 - cell) / 2, j + (1 - cell) / 2
            t, f, r, depth = v3.box_faces(cam, x0, y0, x0 + cell, y0 + cell, 0,
                                          max(hgt, 0.34))
            faces.append((depth, level(c), t, f, r))

    faces.sort(key=lambda b: -b[0])
    dmin = min(b[0] for b in faces)
    dmax = max(b[0] for b in faces)
    for depth, lv, t, f, r in faces:
        k = (dmax - depth) / (dmax - dmin) if dmax > dmin else 1.0
        fog = 0.42 + 0.58 * k
        base = HEAT[lv]
        out.append(v3.poly(t, v3.shade(base, 1.05 * fog)))
        out.append(v3.poly(f, v3.shade(base, 0.44 * fog)))
        out.append(v3.poly(r, v3.shade(base, 0.68 * fog)))

    return "".join(out), cam


def render(d):
    b = [D.plate(W, H), D.grain(W, H)]

    # header
    b.append(M("TELEMETRY", MARGIN, 40, 9, D.ACC, 2.4))
    b.append(M(f"UPDATED {d['updated']}  ·  SOURCE GITHUB API",
               W - MARGIN, 40, 8.5, D.INK3, 2.0, anchor="end"))
    b.append(D.rule(MARGIN, 52, W - MARGIN, 52))

    # headline numbers
    stats = [("CONTRIBUTIONS", d["contributions"]), ("COMMITS", d["commits"]),
             ("PULL REQUESTS", d["prs"]), ("STARS", d["stars"]),
             ("REPOSITORIES", d["repos"]), ("FOLLOWERS", d["followers"])]
    cell = (W - 2 * MARGIN) / len(stats)
    for i, (lab, val) in enumerate(stats):
        x = MARGIN + i * cell
        b.append(T(f"{val:,}", x, 118, 44, D.INK, -1.4))
        b.append(M(lab, x, 140, 8.2, D.INK3, 1.8))
        if i:
            b.append(D.rule(x - 22, 84, x - 22, 148, D.HAIR))
    b.append(D.rule(MARGIN, 164, W - MARGIN, 164))

    # 3D calendar
    b.append(M("CONTRIBUTION CALENDAR — TRAILING 12 MONTHS", MARGIN, 188, 8.5, D.INK3, 2.0))
    b.append(M(f"{d['streak']} DAY STREAK", W - MARGIN, 188, 8.5, D.ACC, 2.0, anchor="end"))
    b.append(f'<ellipse cx="640" cy="350" rx="340" ry="140" fill="url(#cityGlow)"/>')
    weeks = d["weeks"][-53:]
    svg_city, cam = city(weeks, (56, 202, 888, 276))
    b.append(svg_city)

    # month axis: straight baseline, positions taken from the 3D ground plane
    prev, last_x = None, -999
    for i, week in enumerate(weeks):
        if not week:
            continue
        m = int(week[0]["date"][5:7])
        if m != prev:
            px = cam.project((i + 0.5, len(week) / 2, 0))[0]
            if px - last_x > 42:
                b.append(MO(MONTHS[m - 1], px, 496, 7.2, D.INK3, 1.0, anchor="middle"))
                last_x = px
            prev = m
    b.append(D.rule(MARGIN, 514, W - MARGIN, 514))

    # languages
    b.append(M("PRIMARY LANGUAGES BY REPOSITORY", MARGIN, 538, 8.5, D.INK3, 2.0))
    total = sum(c for _, c in d["langs"]) or 1
    top = d["langs"][:6]
    other = total - sum(c for _, c in top)
    segs = list(top) + ([("OTHER", other)] if other else [])

    bx, by, bw, bh = MARGIN, 550, W - 2 * MARGIN, 10
    cx = bx
    for i, (_, count) in enumerate(segs):
        w = bw * count / total
        b.append(f'<rect x="{cx:.1f}" y="{by}" width="{max(w-2,1):.1f}" height="{bh}" rx="2" '
                 f'fill="{LANG_RAMP[min(i, len(LANG_RAMP)-1)]}"/>')
        cx += w

    lx, last_end = bx, -999
    for i, (name, count) in enumerate(segs):
        pct = 100.0 * count / total
        label = f"{name.upper()} {pct:.0f}%"
        lw = MOW(label, 7.6, 1.2)
        if pct >= 7.5:
            px = max(lx, last_end + 12)
            if px + lw > W - MARGIN:
                px = W - MARGIN - lw
            b.append(M(label, px, 578, 7.6, D.INK3 if i > 2 else D.INK2, 1.2))
            last_end = px + lw
        lx += bw * count / total

    b.append(M("RENDERED DAILY FROM LIVE GITHUB DATA BY ACTIONS", MARGIN, 596, 7.2,
               D.INK3, 1.6, opacity=0.7))
    b.append(M("SHAFIUR0", W - MARGIN, 596, 7.2, D.INK3, 1.6, anchor="end", opacity=0.7))

    defs = (D.plate_defs(W, H) +

            f'<radialGradient id="cityGlow" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0%" stop-color="{D.ACC}" stop-opacity="0.11"/>'
            f'<stop offset="60%" stop-color="{D.ACC}" stop-opacity="0.035"/>'
            f'<stop offset="100%" stop-color="{D.ACC}" stop-opacity="0"/></radialGradient>')
    return D.svg(W, H, "".join(b), defs)


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    login = "Shafiur0"
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--token":
            token = args[i + 1]
        if a == "--login":
            login = args[i + 1]
    if not token:
        print("no GITHUB_TOKEN", file=sys.stderr)
        return 1
    data = collect(login, token)
    os.makedirs(OUT, exist_ok=True)
    s = render(data)
    open(os.path.join(OUT, "telemetry.svg"), "w", encoding="utf-8").write(s)
    print(f"telemetry.svg {len(s)} bytes | contributions={data['contributions']} "
          f"stars={data['stars']} streak={data['streak']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
