# Steckbrief Manager V6

## Schnellstart

1. **start.bat** doppelklicken
2. Die App öffnet sich automatisch im Browser unter http://localhost:8080
3. Das Kommandofenster offen lassen, solange die App läuft

## Änderungen in V6

- Neues FOM-Logo (PNG) ohne weißen Hintergrund
- Steckbriefe aus Hochschulentwicklungsplan geladen

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `start.bat` | Startet die App (Python HTTP-Server + Browser) |
| `index.html` | Haupt-Anwendung (Single Page Application) |
| `steckbriefe.json` | Steckbrief-Daten im JSON-Format (29 Steckbriefe) |
| `fom-logo.png` | FOM-Logo |
| `import_steckbriefe.py` | Skript zum Import von DOCX-Steckbriefen |

## Steckbriefe importieren

Um neue Steckbriefe aus DOCX-Dateien zu importieren:

1. DOCX-Dateien in einen Ordner legen
2. `import_steckbriefe.py` anpassen (Pfade ändern)
3. Ausführen: `python import_steckbriefe.py`
4. Die generierte `steckbriefe.json` wird automatisch geladen

## Voraussetzungen

- Python 3.x (für den HTTP-Server)
- python-docx (nur für Import): `pip install python-docx`
- Moderner Webbrowser (Chrome, Firefox, Edge)

## Hinweise

- Daten werden im Browser (localStorage) gespeichert
- Export/Import über die App-Oberfläche möglich
- Zum Zurücksetzen: localStorage im Browser löschen
