# ADR-0001: LDAP-Authentifizierung statt OAuth 2.0 / OpenID Connect

## Status
Accepted

## Kontext
Der BCW-Software-Standard (Stufe 1, §1.2) schreibt OAuth 2.0 / OpenID Connect als Standard-Protokoll für Authentifizierung und Autorisierung vor, mit EntraID als bevorzugter Anbindeschicht.

Der Steckbrief-Manager ist eine interne Anwendung im BCW-Netzwerk mit ca. 20 aktiven Nutzern. Die Authentifizierung erfolgt aktuell direkt gegen das on-premises Active Directory via LDAP.

## Entscheidung
Wir verwenden direkte LDAP-Authentifizierung gegen das on-premises Active Directory statt OAuth 2.0 / OIDC via EntraID.

## Begründung
- Die Anwendung läuft ausschließlich im internen Netzwerk und ist nicht öffentlich erreichbar.
- Der kleine Nutzerkreis (Prozessmanagement-Team) rechtfertigt den zusätzlichen Aufwand für eine OIDC-Anbindung aktuell nicht.
- LDAP-Bind authentifiziert direkt gegen die gleiche Identitätsquelle (Active Directory), die auch nach EntraID synchronisiert wird.
- Passwörter werden nicht in der Anwendung gespeichert – sie werden nur für den LDAP-Bind-Vorgang verwendet und anschließend verworfen.

## Kompensationsmaßnahmen
- JWT-Tokens sind zeitlich begrenzt (konfigurierbar, Standard: 8h).
- JWT_SECRET wird über Umgebungsvariablen/Key Vault konfiguriert, nicht hartcodiert.
- LDAP-Filter-Inputs werden mit `escape_filter_chars` gegen LDAP-Injection geschützt.
- Bei einer zukünftigen Migration auf Docker Swarm / öffentliche Erreichbarkeit muss auf OAuth 2.0 / OIDC umgestellt werden.

## Konsequenzen
- Kein Single Sign-On mit anderen BCW-Anwendungen.
- Kein Token-Refresh via OAuth-Flow – Nutzer müssen sich nach Token-Ablauf erneut anmelden.
- Migration auf OIDC ist als eigene Aufgabe geplant.
