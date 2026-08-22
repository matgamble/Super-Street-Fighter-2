# Android-App

Packt `../index.html` in eine App, die ohne Netz läuft: `ssf2-specials.apk`.

Die App ist nichts weiter als eine WebView im Vollbild, die
`file:///android_asset/index.html` lädt. Deshalb gibt es nur eine einzige
Java-Klasse – die ganze Arbeit macht weiterhin die HTML-Seite.

| | |
|---|---|
| Paketname | `io.github.matgamble.ssf2specials` |
| Name im Launcher | SSF II Specials |
| Berechtigungen | **keine** – die App geht nie ins Netz |
| Läuft ab | Android 7 (API 24), gebaut gegen API 34 |
| Größe | rund 290 KB |

## Installieren

1. `ssf2-specials.apk` auf das Gerät kopieren.
2. Im Dateimanager antippen. Android fragt einmal nach der Erlaubnis,
   Apps aus dieser Quelle zu installieren – das ist bei jeder App
   normal, die nicht aus dem Play Store kommt.
3. Danach liegt „SSF II Specials“ im Launcher.

Auf dem AYN Thor lässt sie sich wie jede andere App auf den unteren Screen
schieben.

## Was die App gegenüber der Webseite anders macht

- **Schriften eingebettet.** Die Web-Fassung holt Anton und Barlow Semi
  Condensed von Google Fonts. `embed_fonts.py` lädt sie beim Bauen herunter und
  legt sie als `data:`-URI in die Seite, damit offline nichts fehlt. Die Datei
  im Repo bleibt unverändert – die Umwandlung passiert nur in `build/`.
- **Vollbild.** Status- und Navigationsleiste sind ausgeblendet, der Screen ist
  knapp genug.
- **Bildschirm bleibt an,** solange die App vorne ist.
- **Systemweite Schriftvergrößerung wird ignoriert** (`setTextZoom(100)`).
  Sonst würde die Seite zweimal skaliert – einmal von Android, einmal von
  ihrer eigenen `fit()`-Routine – und passte nicht mehr auf den Screen.

## Bauen

```bash
cd android && ./build.sh
```

Gebraucht werden `aapt`, `zipalign`, `apksigner`, ein JDK ab 17 und Python 3.
Unter Ubuntu:

```bash
sudo apt install aapt zipalign apksigner default-jdk python3
pip install playwright pillow          # nur für make_icon.py
```

Dazu zwei Dateien in `android/.tools/` (nicht im Repo, zusammen rund 42 MB):

```bash
mkdir -p android/.tools
curl -Lo android/.tools/dx.jar \
  https://repo1.maven.org/maven2/com/jakewharton/android/repackaged/dalvik-dx/16.0.1/dalvik-dx-16.0.1.jar
curl -Lo android/.tools/android.jar \
  https://raw.githubusercontent.com/Reginer/aosp-android-jar/main/android-34/android.jar
```

Beides bewusst **nicht** aus dem Android SDK: `dl.google.com` ist aus der
Umgebung, in der hier gebaut wird, per Netzwerk-Policy gesperrt (auch der
Umweg über `maven.google.com`, das nur dorthin weiterleitet). Maven Central
und `raw.githubusercontent.com` sind erreichbar, also kommen Dexer und
Plattform-JAR von dort; `aapt`, `zipalign` und `apksigner` liefert Ubuntu
selbst mit.

## Stolperstellen, die schon zugeschlagen haben

**`resources.arsc` muss unkomprimiert *und* 4-Byte-ausgerichtet sein.** Sonst
verweigert Android ab Version 11 die Installation, sobald die App API 30 oder
höher anvisiert. `aapt` komprimiert die Datei, deshalb packt `build.sh` das
Archiv einmal um. Danach richtet `zipalign` aus.

**Reihenfolge: erst ausrichten, dann signieren – und nur v2/v3.** Eine
v1-Signatur (JAR-Signing) schreibt `META-INF/*.SF` und `.RSA` nachträglich ins
Archiv und verschiebt damit alles wieder. Darum steht in `build.sh`
`--v1-signing-enabled false`; v2 gibt es seit Android 7 und `minSdkVersion` ist
24, also fehlt nichts.

**Ausrichtung richtig messen.** Die Länge des Extra-Feldes steht zweimal im
ZIP: im lokalen Header und im Zentralverzeichnis. `zipalign` polstert nur den
lokalen Header. Python liefert über `ZipInfo.extra` die Angabe aus dem
Zentralverzeichnis – wer damit rechnet, misst einen falschen Offset und jagt
einem Fehler nach, den es nicht gibt. `check_apk.py` liest deshalb den lokalen
Header direkt.

`check_apk.py` prüft nach jedem Build genau diese Punkte und bricht ab, wenn
etwas nicht stimmt.

## Signaturschlüssel

`debug.keystore` (Passwort `android`, Alias `androiddebugkey`) liegt im Repo,
damit jede neue Fassung mit demselben Schlüssel signiert wird – nur dann
installiert Android sie als Aktualisierung über die alte, ohne sie vorher zu
deinstallieren. Der Schlüssel ist ein reiner Selbstsigner ohne Schutzwert; die
App fordert keine einzige Berechtigung und geht nie ins Netz.

**Falls dieses Repository jemals öffentlich gestellt wird** (etwa für GitHub
Pages): vorher einen neuen Schlüssel erzeugen und `debug.keystore` aus der
Historie entfernen. Ein öffentlich bekannter Schlüssel erlaubt es Fremden, eine
eigene App als Aktualisierung dieser hier auszugeben.

## Dateien

| Datei | Zweck |
|---|---|
| `build.sh` | der ganze Build |
| `AndroidManifest.xml` | Paketname, SDK-Stufen, Start-Activity |
| `src/.../MainActivity.java` | die WebView |
| `res/values/strings.xml` | App-Name |
| `res/mipmap-*/ic_launcher.png` | Launcher-Icon, erzeugt von `make_icon.py` |
| `make_icon.py` | rendert das Icon (die vier Tasten als Raute) |
| `embed_fonts.py` | baut die Offline-Fassung der Seite |
| `check_apk.py` | prüft das fertige APK |
