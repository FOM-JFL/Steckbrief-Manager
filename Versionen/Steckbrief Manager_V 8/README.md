# Steckbrief Manager V8

## Schnellstart

1. **start.bat** doppelklicken
2. Die App installiert automatisch fehlende Python-Pakete (Flask, mysql-connector)
3. API-Server (Port 5000) und Web-Server (Port 8080) werden gestartet
4. Die App öffnet sich automatisch im Browser unter http://localhost:8080
5. Das Kommandofenster offen lassen, solange die App läuft

## Architektur

```
Browser (localhost:8080)  ──►  index.html (Single Page Application)
                                    │
                                    ▼
                              api_server.py (Flask, Port 5000)
                                    │
                                    ▼
                              MariaDB (mariadb.bcw-intern.local)
                              Datenbank: bcw_allgemein
                              Tabelle: t_hochschulsteckbriefe
```

## Änderungen seit V6

- **Datenbankanbindung**: Steckbriefe werden in MariaDB gespeichert statt localStorage
- **Flask REST-API** (`api_server.py`): GET/POST/DELETE Endpoints für Steckbriefe
- **Personen-Autocomplete**: Auftraggeber, Prozessmanager etc. mit FID-Lookup aus `datapool.t_personen`
- **Lohnmandanten-Filter**: Nur aktive Mitarbeitende werden bei Personensuche angezeigt
- **Automatische Änderungshistorie**: Beim Speichern werden geänderte Felder automatisch protokolliert (Datum, Benutzer, Feldnamen)
- **Import in DB**: Word- und JSON-Import schreiben direkt in die Datenbank
- **Neue Batch-Datei**: Startet API-Server und Web-Server; prüft und installiert Abhängigkeiten

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `start.bat` | Startet die App (API-Server + HTTP-Server + Browser) |
| `api_server.py` | Flask REST-API (Schnittstelle zur MariaDB) |
| `index.html` | Haupt-Anwendung (Single Page Application) |
| `steckbriefe.json` | Steckbrief-Daten im JSON-Format (Backup/Import-Quelle) |
| `fom-logo.png` | FOM-Logo |
| `import_steckbriefe.py` | Skript zum Import von DOCX-Steckbriefen in JSON |

## Steckbriefe importieren

### Aus DOCX-Dateien
1. DOCX-Dateien in einen Ordner legen
2. `import_steckbriefe.py` anpassen (Pfade ändern)
3. Ausführen: `python import_steckbriefe.py`

### Über die App
- **JSON-Import**: In der App über das Menü "Importieren > JSON"
- **Word-Import**: In der App über das Menü "Importieren > Word" (Admin)

## Voraussetzungen

- **Python 3.x** (für API- und HTTP-Server)
- **flask**, **flask-cors** (REST-API): `pip install flask flask-cors`
- **mysql-connector-python** (Datenbankzugriff): `pip install mysql-connector-python`
- **python-docx** (nur für DOCX-Import): `pip install python-docx`
- **Moderner Webbrowser** (Chrome, Firefox, Edge)
- **Netzwerkzugang** zu `mariadb.bcw-intern.local` (BCW-Netzwerk)

## Datenbank

- **Host**: mariadb.bcw-intern.local
- **Datenbank**: bcw_allgemein
- **Tabelle**: t_hochschulsteckbriefe (58+ Spalten inkl. FID-Felder und aenderungshistorie)
- **Personen**: datapool.t_personen (Autocomplete-Quelle)
- **Lohnmandanten**: tele_v.t_lohnmandanten (Filterung aktiver Mitarbeitender)

## Hinweise

- Daten werden in der MariaDB gespeichert (nicht mehr localStorage)
- Fallback auf localStorage, wenn API nicht erreichbar
- Änderungshistorie wird automatisch bei jedem Speichern aktualisiert
