import os, sys, subprocess, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "assets", "ds")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def build_preview(theme_bg, theme_fg, path):
    files = sorted(glob.glob(os.path.join(OUT, "*.svg")))
    rows = []
    for f in files:
        name = os.path.basename(f)
        rows.append(f'<div class="row"><div class="cap">{name}</div>'
                    f'<img src="../assets/ds/{name}"></div>')
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<style>
  body{{margin:0;padding:40px 24px;background:{theme_bg};color:{theme_fg};
       font:13px/1.5 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
  .wrap{{max-width:1012px;margin:0 auto}}
  .row{{margin:0 0 26px}}
  .cap{{font:11px/1 ui-monospace,Consolas,monospace;letter-spacing:1.6px;
        text-transform:uppercase;opacity:.45;margin:0 0 8px 2px}}
  img{{width:100%;display:block}}
</style></head><body><div class="wrap">{''.join(rows)}</div></body></html>"""
    open(path, "w", encoding="utf-8").write(html)

def shot(html, png, w, h):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={w},{h}",
                    f"--screenshot={png}", "file:///" + html.replace("\\", "/")],
                   check=False, capture_output=True)

if __name__ == "__main__":
    hp = os.path.join(HERE, "..", "preview", "sheet.html")
    build_preview("#0d1117", "#e6edf3", hp)
    shot(hp, os.path.join(HERE, "..", "preview", "sheet_dark.png"), 1100, 4200)
    build_preview("#ffffff", "#1f2328", hp.replace("sheet", "sheet_light"))
    shot(hp.replace("sheet", "sheet_light"),
         os.path.join(HERE, "..", "preview", "sheet_light.png"), 1100, 4200)
    print("ok")
