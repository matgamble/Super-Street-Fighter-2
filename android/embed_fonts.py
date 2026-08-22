#!/usr/bin/env python3
"""Baut aus ../index.html die Fassung für die App.

Die Web-Fassung holt Anton und Barlow Semi Condensed von Google Fonts. In der
App darf nichts aus dem Netz kommen, also werden die Schriften hier
heruntergeladen, als data:-URI eingebettet und die <link>-Zeilen ersetzt.

Aufruf:  embed_fonts.py <quelle.html> <ziel.html>
"""

import base64
import pathlib
import re
import sys
import urllib.request

CSS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Anton&family=Barlow+Semi+Condensed:wght@400;500;600;700&display=swap"
)
# Nur diese Subsets: mehr braucht die deutschsprachige Seite nicht.
SUBSETS = {"latin", "latin-ext"}
# Browser-UA, sonst liefert Google die alten TTF-Dateien statt woff2.
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

FONT_LINKS = re.compile(
    r'[ \t]*<link[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>\n?', re.I)
FACE_BLOCK = re.compile(
    r'/\*\s*([a-z0-9-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})', re.I)


def fetch(url: str) -> bytes:
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()


def build_font_css() -> str:
    css = fetch(CSS_URL).decode("utf-8")
    out = []
    for subset, block in FACE_BLOCK.findall(css):
        if subset.lower() not in SUBSETS:
            continue
        url_match = re.search(r'url\((https://[^)]+\.woff2)\)', block)
        if not url_match:
            continue
        data = fetch(url_match.group(1))
        uri = "data:font/woff2;base64," + base64.b64encode(data).decode("ascii")
        out.append(block.replace(url_match.group(1), uri))
        print(f"  {subset:10s} {len(data):>7,} Byte  {url_match.group(1).rsplit('/', 1)[-1]}")
    if not out:
        raise SystemExit("Keine passenden @font-face-Blöcke gefunden.")
    return "\n".join(out)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

    html = src.read_text(encoding="utf-8")
    if not FONT_LINKS.search(html):
        raise SystemExit("In der Quelle stehen keine Google-Fonts-<link>-Zeilen.")

    font_css = build_font_css()
    replacement = "<style>\n/* Schriften eingebettet – die App braucht kein Netz. */\n" \
                  + font_css + "\n</style>\n"

    # Erste Fundstelle ersetzen, alle weiteren entfernen.
    html, _ = FONT_LINKS.subn(lambda m: replacement, html, count=1)
    html = FONT_LINKS.sub("", html)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html, encoding="utf-8")
    print(f"  → {dst}  ({len(html):,} Zeichen)")


if __name__ == "__main__":
    main()
