"""Erweitert die Bewertungskriterien-Tabelle um Beschreibungen."""
import mysql.connector

conn = mysql.connector.connect(
    host='mariadb.bcw-intern.local',
    user='HochschulorgaApps',
    password='%z8J9xjZha)9,)Jn',
    database='HochschulorgaApps',
    ssl_disabled=False
)
cursor = conn.cursor()

# Beschreibung-Spalte hinzufügen
try:
    cursor.execute('ALTER TABLE SteckbriefManager_bewertungskriterien ADD COLUMN beschreibung TEXT AFTER bezeichnung')
    print('Spalte beschreibung hinzugefügt')
except Exception as e:
    print('Spalte existiert schon oder Fehler:', e)

# Beschreibungen einfügen
updates = [
    ('bewertung_strategie', '(gesamtbetriebliche Kennziffern, Entscheidungsgrundlagen, Produktivität, Wirtschaftlichkeit, Rentabilität)'),
    ('bewertung_recht', '(Hochschulrecht, Arbeitsrecht, Compliance, DSGVO, GoBD, UStG, Betriebsrat etc.)'),
    ('bewertung_technik', '(bspw. Ablösung VB6)'),
    ('bewertung_kunden', 'Interessenten, Studierende, Teilnehmende|(Digitalisierung von Verwaltungstätigkeiten etc.)'),
    ('bewertung_lehrende', '(Digitalisierung von Verwaltungstätigkeiten etc.)'),
    ('bewertung_lieferanten', '(Anpassungszwänge aufgrund Änderungen an ext. Software etc.)'),
    ('bewertung_mitarbeitende', '(Optimierung der Arbeitsabläufe etc.)'),
]
for feld, beschr in updates:
    cursor.execute('UPDATE SteckbriefManager_bewertungskriterien SET beschreibung = %s WHERE db_feld = %s', (beschr, feld))
    print(f'  {feld}: {cursor.rowcount} Zeile(n) aktualisiert')

conn.commit()
cursor.close()
conn.close()
print('✅ Fertig')
