# ADR-0002: Single-File Frontend ohne Framework

## Status
Accepted

## Kontext
Der BCW-Software-Standard (Stufe 1, §1.3) fordert strukturelle Trennung von Fachlogik und Infrastruktur. Die Anwendung nutzt aktuell ein Single-File-Frontend (`index.html` mit eingebettetem CSS und JavaScript) ohne Build-Tools oder Framework.

## Entscheidung
Das Frontend bleibt als einzelne `index.html`-Datei ohne Framework (React, Angular, Vue o. Ä.) implementiert.

## Begründung
- Die Anwendung ist ein internes Tool mit begrenztem Funktionsumfang und kleinem Nutzerkreis.
- Kein Build-Schritt erforderlich – die Datei wird direkt vom statischen Server ausgeliefert.
- Deployment ist minimal: eine einzelne HTML-Datei + API-Server.
- Die Fachlogik (Validierung, Datenaufbereitung, Export) ist in benannten JavaScript-Funktionen strukturiert und von der DOM-Manipulation getrennt.
- Die Komplexität des Frontends rechtfertigt den Overhead eines Frameworks, Build-Toolchains und Node.js-Dependencies aktuell nicht.

## Konsequenzen
- Keine automatische XSS-Protection durch Framework – manuelle `escapeHtml()`-Aufrufe bei allen dynamisch eingefügten Daten erforderlich.
- Keine Komponenten-Wiederverwendung – Wiederholung von UI-Patterns.
- Bei signifikantem Funktionszuwachs sollte eine Migration auf ein Framework evaluiert werden.
- Unit-Tests für Frontend-Logik sind nur eingeschränkt möglich (kein Modul-System).
