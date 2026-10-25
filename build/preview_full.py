"""Renders README.md with GitHub-ish markdown CSS for visual QA."""
import os, re, subprocess, sys
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """
*{box-sizing:border-box}
body{margin:0;background:%(bg)s;color:%(fg)s;
  font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.markdown-body{max-width:1012px;margin:0 auto;padding:32px 16px 64px;
  font-size:16px;line-height:1.5;word-wrap:break-word}
.markdown-body img{max-width:100%%;box-sizing:content-box;background:transparent}
.markdown-body p{margin:0 0 16px}
.markdown-body br{display:block;content:""}
.markdown-body table{border-collapse:collapse;display:block;width:max-content;
  max-width:100%%;overflow:auto;margin:0 0 16px}
.markdown-body table th,.markdown-body table td{padding:6px 13px;
  border:1px solid %(border)s}
.markdown-body table tr{background:%(bg)s;border-top:1px solid %(border)s}
.markdown-body details{margin:0 0 16px}
.markdown-body summary{cursor:pointer;padding:4px 0;color:%(fg)s}
.markdown-body code{background:%(codebg)s;padding:.2em .4em;border-radius:6px;
  font:85%% ui-monospace,Consolas,monospace}
.markdown-body a{color:%(link)s;text-decoration:none}
.markdown-body a:hover{text-decoration:underline}
.markdown-body sub{font-size:12px;color:%(muted)s}
.markdown-body b{font-weight:600}
"""

THEMES = {
    "dark": dict(bg="#0d1117", fg="#e6edf3", border="#30363d", codebg="#161b22",
                 link="#4493f8", muted="#9198a1"),
    "light": dict(bg="#ffffff", fg="#1f2328", border="#d1d9e0", codebg="#eff1f3",
                  link="#0969da", muted="#59636e"),
}


def build(theme="dark", offset=0):
    src = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    src = src.replace('src="assets/', 'src="../assets/')
    html = markdown.markdown(src, extensions=["tables", "md_in_html", "fenced_code"])
    css = CSS % THEMES[theme]
    if offset:
        css += f"body{{margin-top:-{offset}px}}"
    page = (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}'
            f'</style></head><body><article class="markdown-body">{html}</article>'
            f'</body></html>')
    hp = os.path.join(ROOT, "preview", f"readme_{theme}.html")
    open(hp, "w", encoding="utf-8").write(page)
    return hp


def shot_full(theme="dark", out="readme_full.png", scale=1.0, height=6000):
    hp = os.path.join(ROOT, "preview", f"readme_{theme}.html")
    png = os.path.join(ROOT, "preview", out)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--virtual-time-budget=12000",
                    f"--force-device-scale-factor={scale}", f"--window-size=1044,{height}",
                    f"--screenshot={png}", "file:///" + hp.replace("\\", "/")],
                   capture_output=True)
    print(out, os.path.getsize(png) if os.path.exists(png) else "FAIL")


if __name__ == "__main__":
    build("dark")
    shot_full("dark", "readme_dark.png", 1.0, 5400)
    build("light")
    shot_full("light", "readme_light.png", 1.0, 5400)
    for i, off in enumerate([700, 1500, 2300, 3100, 3900, 4600]):
        build("light", off)
        shot_full("light", f"crop_{i}.png", 1.5, 760)
    build("dark", 1500)
    shot_full("dark", "crop_dark1.png", 1.5, 760)
