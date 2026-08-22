#!/usr/bin/env python3
"""Erzeugt die Launcher-Icons in res/mipmap-*/ic_launcher.png.

Motiv: die vier Aktionstasten in Super-Famicom-Farben als Raute – dasselbe
Layout wie auf dem Gerät und dieselbe Farbsprache wie in der App.
Einmal in 512 px gerendert und dann auf die Dichtestufen verkleinert.
"""

import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
CHROMIUM = "/opt/pw-browsers/chromium"

DENSITIES = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}

ICON_HTML = """
<style>
  html,body{margin:0;background:transparent}
  .icon{
    width:512px; height:512px; position:relative;
    border-radius:112px;
    background:
      radial-gradient(circle at 50% 38%, #2A2159 0%, #171232 55%, #0C0A1A 100%);
    box-shadow:inset 0 0 0 10px #FFB627, inset 0 0 0 16px #0C0A1A;
  }
  .btn{
    position:absolute; width:118px; height:118px; border-radius:50%;
    left:50%; top:50%; margin:-59px 0 0 -59px;
    box-shadow:0 6px 0 rgba(0,0,0,.45), inset 0 8px 0 rgba(255,255,255,.28);
  }
  .a{background:#FF3B41; transform:translateY(-122px)}
  .b{background:#FFC93C; transform:translateX(122px)}
  .y{background:#3FBF6A; transform:translateY(122px)}
  .x{background:#4A8CFF; transform:translateX(-122px)}
</style>
<div class="icon">
  <div class="btn a"></div>
  <div class="btn b"></div>
  <div class="btn y"></div>
  <div class="btn x"></div>
</div>
"""


def main():
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image
    except ImportError:
        sys.exit("Bitte zuerst installieren:  pip install playwright pillow")

    tmp = HERE / ".tools" / "icon.html"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(ICON_HTML, encoding="utf-8")

    base = HERE / ".tools" / "icon-512.png"
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM)
        page = browser.new_page(viewport={"width": 512, "height": 512})
        page.goto(tmp.as_uri())
        page.wait_for_timeout(300)
        page.locator(".icon").screenshot(path=str(base), omit_background=True)
        browser.close()

    src = Image.open(base).convert("RGBA")
    for density, size in DENSITIES.items():
        out_dir = HERE / "res" / f"mipmap-{density}"
        out_dir.mkdir(parents=True, exist_ok=True)
        src.resize((size, size), Image.LANCZOS).save(out_dir / "ic_launcher.png")
        print(f"  res/mipmap-{density}/ic_launcher.png  ({size}x{size})")


if __name__ == "__main__":
    main()
