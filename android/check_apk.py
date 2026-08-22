#!/usr/bin/env python3
"""Prüft die Stellen im fertigen APK, an denen Android beim Installieren aussteigt.

Aufruf:  check_apk.py <datei.apk>
"""

import struct
import sys
import zipfile

REQUIRED = ["AndroidManifest.xml", "classes.dex", "resources.arsc", "assets/index.html"]

LOCAL_HEADER = struct.Struct("<IHHHHHIIIHH")


def data_offset(apk: str, info: zipfile.ZipInfo) -> int:
    """Offset der Nutzdaten im Archiv.

    Wichtig: die Längen von Name und Extra-Feld aus dem *lokalen* Header lesen.
    zipalign polstert das Extra-Feld genau dort, im Zentralverzeichnis steht
    weiterhin die ungepolsterte Länge – wer die nimmt, misst falsch.
    """
    with open(apk, "rb") as f:
        f.seek(info.header_offset)
        fields = LOCAL_HEADER.unpack(f.read(LOCAL_HEADER.size))
    name_len, extra_len = fields[9], fields[10]
    return info.header_offset + LOCAL_HEADER.size + name_len + extra_len


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    apk = sys.argv[1]

    with zipfile.ZipFile(apk) as z:
        names = set(z.namelist())
        missing = [n for n in REQUIRED if n not in names]
        if missing:
            raise SystemExit("    FEHLER: im Archiv fehlt: " + ", ".join(missing))

        arsc = z.getinfo("resources.arsc")
        if arsc.compress_type != zipfile.ZIP_STORED:
            raise SystemExit("    FEHLER: resources.arsc ist komprimiert – "
                             "Android 11+ lehnt die Installation ab.")
        off = data_offset(apk, arsc)
        if off % 4:
            raise SystemExit(f"    FEHLER: resources.arsc liegt auf Offset {off}, "
                             "nicht durch 4 teilbar – Android 11+ lehnt die Installation ab.")

        page = z.read("assets/index.html").decode("utf-8")
        if "fonts.googleapis.com" in page or "fonts.gstatic.com" in page:
            raise SystemExit("    FEHLER: assets/index.html lädt noch Schriften aus dem Netz.")
        if page.count("@font-face") < 4:
            raise SystemExit("    FEHLER: in assets/index.html fehlen eingebettete Schriften.")

        print(f"    resources.arsc  unkomprimiert und ausgerichtet (Offset {off})")
        print(f"    assets/index.html  {len(page):,} Zeichen, "
              f"{page.count('@font-face')} Schriftschnitte eingebettet, keine Netzzugriffe")
        print(f"    Archiv  {len(names)} Einträge")


if __name__ == "__main__":
    main()
