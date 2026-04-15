"""
Migration: Neue Spalte 'auftraggeber_multi' hinzufügen und
bestehende auftraggeberFID-Werte als JSON-Array migrieren.
"""
import mysql.connector
import json
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'mariadb.bcw-intern.local'),
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASS'],
    'database': os.environ.get('DB_NAME', 'bcw_allgemein'),
    'ssl_disabled': False
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)

# 1. Prüfen ob Spalte bereits existiert
cursor.execute("""
    SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 't_hochschulsteckbriefe' AND COLUMN_NAME = 'auftraggeber_multi'
""", (DB_CONFIG['database'],))
exists = cursor.fetchone()

if not exists:
    print("Spalte 'auftraggeber_multi' wird hinzugefügt...")
    cursor.execute("ALTER TABLE t_hochschulsteckbriefe ADD COLUMN auftraggeber_multi TEXT NULL AFTER auftraggeberFID")
    conn.commit()
    print("Spalte hinzugefügt.")
else:
    print("Spalte 'auftraggeber_multi' existiert bereits.")

# 2. Bestehende auftraggeberFID-Werte migrieren
cursor.execute("""
    SELECT s.id, s.auftraggeberFID, s.auftraggeber_multi,
           p.Vorname, p.Nachname, p.Titel_de
    FROM t_hochschulsteckbriefe s
    LEFT JOIN datapool.t_personen p ON s.auftraggeberFID = p.PersonenID
    WHERE s.auftraggeberFID IS NOT NULL AND (s.auftraggeber_multi IS NULL OR s.auftraggeber_multi = '')
""")
rows = cursor.fetchall()

migrated = 0
for row in rows:
    name_parts = [row['Titel_de'], row['Vorname'], row['Nachname']]
    name = ' '.join(p for p in name_parts if p)
    if not name:
        name = f"PersonenID {row['auftraggeberFID']}"
    
    multi_json = json.dumps([{"fid": int(row['auftraggeberFID']), "name": name}])
    cursor.execute(
        "UPDATE t_hochschulsteckbriefe SET auftraggeber_multi = %s WHERE id = %s",
        (multi_json, row['id'])
    )
    print(f"  ID {row['id']}: auftraggeberFID={row['auftraggeberFID']} → {multi_json}")
    migrated += 1

conn.commit()
print(f"\n{migrated} Steckbriefe migriert.")

# 3. Übersicht
cursor.execute("SELECT id, auftraggeberFID, auftraggeber_multi FROM t_hochschulsteckbriefe ORDER BY id")
for row in cursor.fetchall():
    print(f"  ID {row['id']}: FID={row['auftraggeberFID']}, multi={row['auftraggeber_multi']}")

conn.close()
print("\nMigration abgeschlossen.")
