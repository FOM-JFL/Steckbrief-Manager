# Steckbrief Manager – Version 9.0.0

## Voraussetzungen

- **Python 3.x** (im PATH)
- **Python-Pakete**: `flask`, `flask-cors`, `mysql-connector-python`
- **Netzwerkzugang** zur MariaDB (`mariadb.bcw-intern.local`)

## Schnellstart

1. `start.bat` doppelklicken
2. Die Batch-Datei:
   - Prüft Python und installiert ggf. fehlende Pakete
   - Startet den API-Server (Port 5000)
   - Startet den HTTP-Server (Port 8080)
   - Öffnet automatisch den Browser unter `http://localhost:8080`
3. **Fenster nicht schließen**, solange die App laufen soll.

## Dateien

| Datei | Beschreibung |
|---|---|
| `start.bat` | Start-Skript (startet API + HTTP-Server, öffnet Browser) |
| `api_server.py` | Flask-REST-API (Brücke zwischen Frontend und MariaDB) |
| `index.html` | Komplettes Frontend (Single-Page-App) |
| `import_steckbriefe.py` | Import-Skript: DOCX-Steckbriefe → JSON |
| `steckbriefe.json` | JSON-Backup / Fallback-Daten |
| `fom-logo.png` | FOM-Logo für das Frontend |
| `VERSION` | Versionsnummer |
| `Rahmengebendes/` | Quelldokumente (DOCX-Steckbriefe für Import) |

## Neue Features in V9

- **Bearbeiter-Zuweisung**: Admins können pro Steckbrief Bearbeiter zuweisen (Personen-Autocomplete)
- **Visuelle Editor-Unterscheidung**: Editoren sehen, welche Steckbriefe sie bearbeiten können
- **Automatische Änderungshistorie**: Änderungen werden automatisch protokolliert (Feld, Benutzer, Zeitstempel)
- **Partial Update**: API aktualisiert nur gesendete Felder (kein Datenverlust bei Teilupdates)

## Datenbank

- Host: `mariadb.bcw-intern.local`
- Datenbank: `bcw_allgemein`
- Tabelle: `t_hochschulsteckbriefe`
- Personen: `datapool.t_personen` (Lohnmandanten-gefiltert)
