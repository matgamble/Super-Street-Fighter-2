# Super Street Fighter II – Specials & Training für den zweiten Screen

Eine einzelne, in sich geschlossene HTML-Seite (`index.html`) für alle 16 Charaktere aus
**Super Street Fighter II – The New Challengers (SNES)**.

Gebaut für den unteren Bildschirm des **AYN Thor** (3,92", 1080 × 1240): oben läuft das
Spiel, unten liegt die Seite. Sie **scrollt nicht** – der Inhalt skaliert sich so, dass
er auf einen Blick auf den Screen passt.

## Drei Ansichten

| Reiter | Inhalt |
|---|---|
| **Specials** | Alle Spezialangriffe mit Richtungspfeilen und den SNES-Knöpfen |
| **Training** | Die Stärke des Charakters plus drei aufeinander aufbauende Übungen – jede mit den Eingaben, um die es geht |
| **Tasten** | Knopfbelegung, Richtungs- und Ladebewegungs-Notation |

Die Trainingsübungen sind bewusst als Reihenfolge nummeriert: Übung 1 legt die Grundlage,
Übung 3 setzt sie im Kampf ein.

## Benutzen

- **Lokal:** `index.html` auf dem Gerät speichern und im Browser öffnen. Funktioniert
  ohne Internet; nur die beiden Schriften (Anton, Barlow Semi Condensed) kommen dann
  aus dem System statt von Google Fonts.
- **Als feste Adresse:** Repository auf öffentlich stellen und in den Repo-Einstellungen
  unter *Pages* die Quelle auf `main` / Root setzen. Danach ist die Seite unter
  `https://matgamble.github.io/Super-Street-Fighter-2/` erreichbar.

## Bedienung

| | |
|---|---|
| Charakter wechseln | `‹` / `›` oder auf den Namen tippen (Vollbild-Auswahl) |
| Ansicht wechseln | die drei Reiter |
| Vollbild | `⛶` oben rechts |
| Tastatur | `←` `→` Charakter, `1` `2` `3` Ansicht, `Esc` Auswahl schließen |

Charakter und zuletzt gewählte Ansicht werden im Browser gespeichert (`localStorage`)
und beim nächsten Öffnen wiederhergestellt.

## Notation

Alle Richtungen gelten für **Blick nach rechts**: `→` heißt immer „zum Gegner hin".

- Drei Knöpfe nebeneinander (Y X L bzw. B A R) = **einer davon genügt**. Der schwache
  ist schnell, der starke stärker und langsamer.
- Rot umrandete Felder = **Ladebewegung**: Richtung ca. 2 Sekunden halten, dann die
  Folgeeingabe.
- SNES-Standardbelegung: `Y` Punch schwach, `X` Punch mittel, `L` Punch stark,
  `B` Kick schwach, `A` Kick mittel, `R` Kick stark.

## Stand der Movelist

Die Liste bildet **Super Street Fighter II – The New Challengers** ab, also das
SNES-Modul – nicht Super Turbo. Bewusst **nicht** enthalten, weil erst ab Super Turbo
im Spiel:

- Zangief: Banishing Flat
- Fei Long: Chicken Wing
- Dee Jay: Machine Gun Upper
- Super-Combos (gibt es in dieser Fassung überhaupt nicht)

Zusammengetragen aus öffentlichen Movelists (GameFAQs, StrategyWiki, Street Fighter
Wiki, SuperCombo Wiki). Es sind keine Grafiken oder Texte aus dem Spiel übernommen –
die Seite enthält ausschließlich selbst geschriebene Inhalte, Zeichen und Farben.

## Technisch

- Eine Datei, kein Build, keine Abhängigkeiten. Die Daten stehen als `ROSTER`-Array im
  `<script>`-Block: pro Charakter `moves` (Eingaben), `strength` (eine Zeile) und
  `drills` (drei Übungen).
- Eingaben sind Token-Listen: `D` Richtung, `C` Ladebewegung, `M` Bewegung als Text,
  `K` Knöpfe, `T` Zusatz. Eine Karte kann mit `seq2` eine zweite Eingabezeile zeigen
  (z. B. Dhalsims Teleport vor/zurück).
- Trainingsübungen verweisen über `use` auf die Moves, deren Eingaben sie zeigen sollen –
  per Move-Name, mit `#2` für dessen zweite Eingabezeile (z. B. `"Yoga Teleport#2"`).
  Die Eingaben werden dort kompakter dargestellt (kleinere Felder, ohne den Zusatz
  „eine davon"). Drei Übungen ohne festen Move (Kens Eckendruck, Dhalsims Abstandsrunde,
  Vegas Klauendistanz) haben bewusst kein `use`.

### Wie „kein Scrollen" funktioniert

`fit()` sucht die größte Schriftgröße, bei der der Inhalt noch in die Bühne passt: Es
läuft von `--fs = 1.40` in Schritten abwärts und nimmt die erste Stufe ohne Überlauf
(von groß nach klein, damit die erste passende auch die größtmögliche ist).

Bleibt die Schrift dabei unter `MIN_READABLE`, schaltet die Bühne in den **Sparmodus**
(`.tight`): Auf der Specials-Ansicht verschwindet der erklärende Fließtext, damit die
Eingaben groß bleiben. Trainingskarten behalten ihn – dort *ist* der Text der Inhalt.
Passt selbst das nicht (sehr kleiner oder sehr kurzer Screen), wird Scrollen als
Rückfallebene erlaubt, statt unlesbar klein zu werden.

Alle Maße innerhalb der Bühne hängen deshalb an `--u` (`calc(var(--fs) * 16px)`) bzw.
an `em`. Elemente, die **selbst** eine `font-size` setzen (`.key`, `.dir`, `.num`),
müssen ihre Breite/Höhe über `calc(var(--u) * n)` angeben – mit `em` würde sich die
Skalierung dort doppelt multiplizieren.

Neu getestet wird am einfachsten so: alle 16 Charaktere × 3 Ansichten durchklicken und
prüfen, dass `stage.scrollHeight <= stage.clientHeight` bleibt.

### Weitere Hinweise

- Richtungspfeile sind Inline-SVG und werden über das SVG-Attribut
  `transform="rotate(winkel 6 6)"` gedreht – **nicht** per CSS-`transform`: bei einem
  `<svg>`-Element liegt der Drehpunkt sonst nicht zuverlässig in der Mitte.
- Die Seite ist bewusst einfarbig dunkel gehalten (Spielbegleiter im Dunkeln), es gibt
  also absichtlich kein helles Farbschema.
- Die Knopffarben entsprechen der Super-Famicom-Belegung und damit den Tasten des
  AYN Thor: A rot, B gelb, X blau, Y grün.

### Als Claude-Artifact veröffentlichen

Beim Veröffentlichen als Artifact darf die Datei **kein** `<!doctype>`, `<html>`,
`<head>` oder `<body>` enthalten – dieser Rahmen wird von der Artifact-Plattform selbst
ergänzt. Für ein Update also aus `index.html` alles zwischen `<title>` und `</style>`
sowie den Body-Inhalt ohne die Rahmen-Tags übernehmen.
