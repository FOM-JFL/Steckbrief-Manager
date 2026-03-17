# Steckbrief Manager V4

**Überblick über die Prozess-/Projektsteckbriefe der FOM**

## Version 4.0.0

### Neuerungen in dieser Version
- Vollständig responsive Design (Desktop + Mobile)
- FOM Corporate Design implementiert
- Hamburger-Menü für mobile Navigation
- Touch-optimierte Buttons (min. 44px)
- Klappbare Filterleiste auf mobilen Geräten
- FOM Logo rechts oben eingebunden
- Optimierte Detailansicht für alle Bildschirmgrößen

## Start der App

### Windows
Doppelklick auf `start.bat` oder `index.html`

### Manuell
Die Datei `index.html` im Browser öffnen.

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `index.html` | Hauptanwendung (Single-Page-App) |
| `steckbriefe.json` | Beispieldaten zum automatischen Laden |
| `start.bat` | Windows-Startdatei |
| `import_steckbriefe.py` | Python-Skript zum Importieren von Word-Steckbriefen |
| `VERSION` | Aktuelle Versionsnummer |

## Funktionen

- **Übersicht**: Kachel- oder Tabellenansicht aller Steckbriefe
- **Filter**: Nach Prozesscluster, Auftraggeber, Status
- **Suche**: Volltextsuche über alle Felder
- **Detailansicht**: Vollständige Anzeige eines Steckbriefs
- **Bearbeitung**: Mit Login als Admin oder Bearbeiter
- **Export**: PDF oder Word-Dokument

## Login

- **Admin**: Passwort `Admin2026!` (alle Rechte)
- **Bearbeiter**: Name eingeben (nur zugewiesene Steckbriefe)

## Technische Hinweise

- Daten werden im Browser-LocalStorage gespeichert
- Keine Server-Installation erforderlich
- Funktioniert offline nach erstem Laden
