"""Renders assets/ds/telemetry.svg from live GitHub data.

Usage:  python gen_telemetry.py [--token TOKEN] [--login USER]
Falls back to GITHUB_TOKEN env var. Exits 1 on failure so CI surfaces it.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

import ds as D
from ds import T, M, MO, MOW, TW

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ds")
W, H = 1000, 424
MARGIN = 48

API = "https://api.github.com"
GQL = "https://api.github.com/graphql"

LANG_RAMP = ["#FF4B1F", "#D9511E", "#B04520", "#87391F", "#5F2F1D", "#3A3A44", "#2A2A32"]
HEAT = ["#16161B", "#4C2417", "#7E2E16", "#BC3C18", "#FF4B1F"]

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

    # current streak
    days = [d for w in weeks for d in w]
    days.sort(key=lambda d: d["date"])
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


def render(d):
    b = [D.plate(W, H)]

    # ── header ─────────────────────────────────────────────────────────────
    b.append(M("TELEMETRY", MARGIN, 40, 9, D.ACC, 2.4))
    b.append(M(f"UPDATED {d['updated']}  ·  SOURCE GITHUB API",
               W - MARGIN, 40, 8.5, D.INK3, 2.0, anchor="end"))
    b.append(D.rule(MARGIN, 52, W - MARGIN, 52))

    # ── headline numbers ───────────────────────────────────────────────────
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
    b.append(D.rule(MARGIN, 166, W - MARGIN, 166))

    # ── contribution calendar ──────────────────────────────────────────────
    b.append(M("CONTRIBUTION CALENDAR — TRAILING 12 MONTHS", MARGIN, 190, 8.5, D.INK3, 2.0))
    b.append(M(f"{d['streak']} DAY STREAK", W - MARGIN, 190, 8.5, D.ACC, 2.0, anchor="end"))

    weeks = d["weeks"][-53:]
    pitch, size = 13.0, 10.0
    gx, gy = MARGIN, 210
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    prev, last_x = None, -999
    for wi, week in enumerate(weeks):
        if not week:
            continue
        first = week[0]["date"]
        m = int(first[5:7])
        mx = gx + wi * pitch
        if m != prev and mx - last_x > 34:
            b.append(MO(months[m - 1], mx, 204, 7.2, D.INK3, 1.0))
            last_x = mx
        if m != prev:
            prev = m
        for di, day in enumerate(week):
            c = day["contributionCount"]
            lvl = 0 if c == 0 else 1 if c < 3 else 2 if c < 7 else 3 if c < 12 else 4
            b.append(f'<rect x="{gx + wi*pitch}" y="{gy + di*pitch}" width="{size}" '
                     f'height="{size}" rx="2" fill="{HEAT[lvl]}"/>')

    b.append(D.rule(MARGIN, 320, W - MARGIN, 320))

    # ── languages ──────────────────────────────────────────────────────────
    b.append(M("PRIMARY LANGUAGES BY REPOSITORY", MARGIN, 344, 8.5, D.INK3, 2.0))
    total = sum(c for _, c in d["langs"]) or 1
    top = d["langs"][:6]
    other = total - sum(c for _, c in top)
    segs = [(n, c) for n, c in top] + ([("OTHER", other)] if other else [])

    bx, by, bw, bh = MARGIN, 358, W - 2 * MARGIN, 10
    cx = bx
    for i, (name, count) in enumerate(segs):
        w = bw * count / total
        b.append(f'<rect x="{cx:.1f}" y="{by}" width="{max(w-2, 1):.1f}" height="{bh}" rx="2" '
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
            b.append(M(label, px, 388, 7.6, D.INK3 if i > 2 else D.INK2, 1.2))
            last_end = px + lw
        lx += bw * count / total

    b.append(M("AUTO-GENERATED DAILY BY GITHUB ACTIONS", MARGIN, 410, 7.2, D.INK3, 1.6, opacity=0.75))
    b.append(M("SHAFIUR0", W - MARGIN, 410, 7.2, D.INK3, 1.6, anchor="end", opacity=0.75))

    defs = (f'<clipPath id="tc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15"/>'
            f'</clipPath>')
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
          f"stars={data['stars']} streak={data['streak']} langs={data['langs'][:3]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
