# Steckbrief-Manager

Webbasiertes Tool zur Verwaltung von Prozess- und Projektsteckbriefen der BCW-Gruppe. Ermöglicht das Erstellen, Bearbeiten, Bewerten und Exportieren von Steckbriefen mit Zeitplan-/Gantt-Ansicht und Portfolio-Übersicht. Zielgruppe: Prozessmanagement-Team und Projektverantwortliche.

## Verantwortlichkeit

- **Owner:** Julia Flor, Team Prozessmanagement
- **Kontakt:** julia.flor@fom.de
- **Support/Oncall:** Best Effort via E-Mail an Owner; Eskalation über Teamleitung Prozessmanagement

## Scope & Systemkontext

- **Was macht der Service?** CRUD-Anwendung für Hochschulsteckbriefe mit AD-Authentifizierung, Rollenverwaltung, PDF-/Word-/Excel-Export und Gantt-Visualisierung.
- **Abhängigkeiten (Up-/Downstream):**
  - MariaDB `bcw_allgemein.t_hochschulsteckbriefe` (Steckbrief-Daten)
  - MariaDB `datapool.t_personen` (Personen-Lookup)
  - Active Directory / LDAP `bcw-intern.local` (Authentifizierung)
- **Nicht im Scope:** Stammdatenpflege (Personen), LDAP-User-Verwaltung

## Tech Stack

- **Backend:** Python 3.12, Flask (REST-API), mysql-connector-python, ldap3, PyJWT
- **Frontend:** Vanilla JavaScript (Single-File `index.html`), jsPDF, docx, xlsx
- **Statischer Server:** Python `http.server`
- **Datenbank:** MariaDB
- **Auth:** AD/LDAP + JWT

## Rollback

Vorheriges Docker-Image-Tag redeployen. Die Anwendung hat keine eigenen DB-Migrationen im Startprozess – Schema-Änderungen werden separat über Migrationsskripte durchgeführt und sind vorwärtskompatibel.

## Dependencies & Schwachstellenmanagement

- **Haupt-Dependencies:**
  - flask, flask-cors (Web-Framework)
  - mysql-connector-python (DB-Zugriff)
  - ldap3 (AD-Authentifizierung)
  - PyJWT (Token-basierte Auth)
  - python-dotenv (Lokale Konfiguration)
- **Prüfung:** `pip audit` für bekannte Vulnerabilities

## Architekturentscheidungen (ADRs)

- [ADR-0001 – LDAP-Authentifizierung statt OAuth/OIDC](./docs/adr/ADR-0001-ldap-auth.md)
- [ADR-0002 – Single-File Frontend ohne Framework](./docs/adr/ADR-0002-single-file-frontend.md)
