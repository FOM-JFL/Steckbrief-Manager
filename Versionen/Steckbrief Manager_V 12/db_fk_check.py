import mysql.connector

conn = mysql.connector.connect(
    host='mariadb.bcw-intern.local',
    user='ralf.schmitz',
    password='d-kvsl1715',
    database='bcw_allgemein',
    ssl_disabled=False
)
cursor = conn.cursor()

# Prüfe Fremdschlüssel-Beziehungen
cursor.execute("""
    SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_SCHEMA, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = 'bcw_allgemein'
    AND TABLE_NAME = 't_hochschulsteckbriefe'
    AND REFERENCED_TABLE_NAME IS NOT NULL
""")
fks = cursor.fetchall()
if fks:
    for fk in fks:
        print(f"{fk[1]} -> {fk[2]}.{fk[3]}.{fk[4]}")
else:
    print("Keine Fremdschlüssel definiert")

# Prüfe ob Historie-Tabelle existiert
cursor.execute("SHOW TABLES LIKE '%historie%'")
tables = cursor.fetchall()
if tables:
    for t in tables:
        print(f"Historie-Tabelle: {t[0]}")
        cursor.execute(f"DESCRIBE {t[0]}")
        for col in cursor.fetchall():
            print(f"  {col[0]:30s} | {col[1]}")
else:
    print("Keine Historie-Tabelle gefunden")

conn.close()
