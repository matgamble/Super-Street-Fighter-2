#!/usr/bin/env bash
# Baut ssf2-specials.apk aus ../index.html.
#
# Voraussetzungen (siehe README.md im selben Ordner):
#   aapt, zipalign, apksigner   – Ubuntu: apt install aapt zipalign apksigner
#   Java (JDK 17 oder neuer)
#   .tools/android.jar          – Android-Plattform-JAR (API 34)
#   .tools/dx.jar               – Dexer
set -euo pipefail
cd "$(dirname "$0")"

PKG=io.github.matgamble.ssf2specials
OUT=build
APK=ssf2-specials.apk
TOOLS=.tools

for t in aapt zipalign apksigner java javac python3; do
  command -v "$t" >/dev/null || { echo "Fehlt: $t"; exit 1; }
done
for f in "$TOOLS/android.jar" "$TOOLS/dx.jar"; do
  [ -f "$f" ] || { echo "Fehlt: $f – siehe README.md"; exit 1; }
done

rm -rf "$OUT" "$APK"
mkdir -p "$OUT/assets" "$OUT/classes"

echo "==> Icons"
[ -f res/mipmap-xxhdpi/ic_launcher.png ] || python3 make_icon.py

echo "==> Seite mit eingebetteten Schriften"
python3 embed_fonts.py ../index.html "$OUT/assets/index.html"

echo "==> Java übersetzen"
javac --release 8 -nowarn -Xlint:-options \
      -classpath "$TOOLS/android.jar" \
      -d "$OUT/classes" \
      $(find src -name '*.java')

echo "==> Dex erzeugen"
java -cp "$TOOLS/dx.jar" com.android.dx.command.Main \
     --dex --min-sdk-version=24 --output="$OUT/classes.dex" "$OUT/classes"

echo "==> Ressourcen und Manifest paketieren"
aapt package -f \
     -M AndroidManifest.xml \
     -S res \
     -A "$OUT/assets" \
     -I "$TOOLS/android.jar" \
     -F "$OUT/raw.apk"
( cd "$OUT" && aapt add -f raw.apk classes.dex >/dev/null )

echo "==> resources.arsc unkomprimiert ablegen"
# Ab Ziel-API 30 verweigert Android die Installation, wenn resources.arsc
# komprimiert im Archiv liegt. aapt komprimiert sie, also einmal umpacken.
python3 - "$OUT/raw.apk" "$OUT/store.apk" <<'PY'
import shutil, sys, zipfile
src, dst = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w") as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        keep = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        keep.external_attr = info.external_attr
        keep.compress_type = (zipfile.ZIP_STORED
                              if info.filename == "resources.arsc"
                              else info.compress_type)
        zout.writestr(keep, data)
PY

echo "==> Ausrichten"
zipalign -f 4 "$OUT/store.apk" "$OUT/aligned.apk"

echo "==> Signieren"
[ -f debug.keystore ] || keytool -genkeypair -v \
  -keystore debug.keystore -storepass android -keypass android \
  -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10950 \
  -dname "CN=SSF II Specials, OU=privat, O=privat, L=Augsburg, C=DE"
# Bewusst nur v2/v3: Eine v1-Signatur schreibt META-INF-Einträge nachträglich
# ins Archiv und zerstört damit die Ausrichtung von zipalign. Ohne
# unkomprimierte UND 4-Byte-ausgerichtete resources.arsc verweigert Android ab
# Version 11 die Installation. v2 gibt es seit Android 7, minSdk ist 24.
apksigner sign \
  --ks debug.keystore --ks-pass pass:android --key-pass pass:android \
  --ks-key-alias androiddebugkey \
  --min-sdk-version 24 \
  --v1-signing-enabled false --v2-signing-enabled true --v3-signing-enabled true \
  --out "$APK" "$OUT/aligned.apk"

echo "==> Prüfen"
python3 check_apk.py "$APK"
apksigner verify --min-sdk-version 24 --verbose "$APK" | sed 's/^/    /'
aapt dump badging "$APK" | grep -E "^(package|application-label|sdkVersion|targetSdkVersion|launchable-activity|uses-permission)" | sed 's/^/    /'
echo
ls -lh "$APK"
echo "Fertig: $(pwd)/$APK"
