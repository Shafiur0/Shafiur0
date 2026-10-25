"""Screenshot helper: renders selected assets to PNG at a given scale."""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def vh(name, width):
    head = open(os.path.join(ROOT, "assets", "ds", name), encoding="utf-8").read(400)
    import re
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
    return width * float(m.group(2)) / float(m.group(1))


def sheet(names, out, scale=1.5, bg="#0d1117", width=1012, gap=22):
    rows = "".join(
        f'<img src="../assets/ds/{n}" style="width:100%;display:block;margin:0 0 {gap}px">'
        for n in names)
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'html,body{{margin:0;background:{bg}}}'
            f'.w{{width:{width}px;padding:0;margin:0 auto}}</style></head>'
            f'<body><div class="w">{rows}</div></body></html>')
    hp = os.path.join(ROOT, "preview", "_shot.html")
    open(hp, "w", encoding="utf-8").write(html)
    png = os.path.join(ROOT, "preview", out)
    total = int(sum(vh(n, width) for n in names) + gap * len(names)) + 8
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}",
                    f"--window-size={width},{total}",
                    f"--screenshot={png}", "file:///" + hp.replace("\\", "/")],
                   capture_output=True)
    print(out, total, os.path.getsize(png) if os.path.exists(png) else "FAIL")


if __name__ == "__main__":
    groups = {
        "g_top.png": ["cover.svg", "nav-01.svg", "nav-02.svg"],
        "g_heads.png": ["head-01.svg", "spec.svg", "head-02.svg", "stack.svg"],
        "g_cards.png": ["head-03.svg", "card-01.svg", "card-02.svg"],
        "g_awards.png": ["head-04.svg", "awards.svg", "footer.svg"],
    }
    for out, names in groups.items():
        sheet(names, out)
