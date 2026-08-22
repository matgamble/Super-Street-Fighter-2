# Super Street Fighter II – Specials für den zweiten Screen

Eine einzelne, in sich geschlossene HTML-Seite (`index.html`), die alle Spezialangriffe
aller 16 Charaktere aus **Super Street Fighter II – The New Challengers (SNES)** zeigt.

Gedacht für den unteren Bildschirm des **AYN Thor**: oben läuft das Spiel, unten liegt
die Seite im Browser. Charakter antippen → alle Specials mit Richtungspfeilen und den
SNES-Knöpfen.

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
| Charakter wählen | Leiste „Charakter wechseln" antippen |
| Blättern | Pfeiltasten ← / → |
| Schriftgröße | die drei **A**-Knöpfe oben rechts |
| Vollbild | Knopf „Vollbild" |
| Tastenbelegung | Leiste am unteren Rand aufklappen |

Die zuletzt gewählte Figur, die Schriftgröße und der Zustand der Legende werden im
Browser gespeichert (`localStorage`) und beim nächsten Öffnen wiederhergestellt.

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

- Eine Datei, kein Build, keine Abhängigkeiten. Die Movelist steht als `ROSTER`-Array
  im `<script>`-Block, die Eingaben als Token-Liste (`D` Richtung, `C` Ladebewegung,
  `M` Bewegung als Text, `K` Knöpfe, `T` Zusatz).
- Richtungspfeile sind Inline-SVG und werden über das SVG-Attribut
  `transform="rotate(winkel 6 6)"` gedreht – **nicht** per CSS-`transform`: bei einem
  `<svg>`-Element liegt der Drehpunkt sonst nicht zuverlässig in der Mitte.
- Die Seite ist bewusst einfarbig dunkel gehalten (Spielbegleiter im Dunkeln), es gibt
  also absichtlich kein helles Farbschema.

### Als Claude-Artifact veröffentlichen

Beim Veröffentlichen als Artifact darf die Datei **kein** `<!doctype>`, `<html>`,
`<head>` oder `<body>` enthalten – dieser Rahmen wird von der Artifact-Plattform selbst
ergänzt. Für ein Update also aus `index.html` alles zwischen `<title>` und `</style>`
sowie den Body-Inhalt ohne die Rahmen-Tags übernehmen.
