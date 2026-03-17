import mysql.connector

conn = mysql.connector.connect(
    host='mariadb.bcw-intern.local',
    user='ralf.schmitz',
    password='d-kvsl1715',
    database='datapool',
    ssl_disabled=False
)
cursor = conn.cursor()
cursor.execute("DESCRIBE t_personen")
cols = cursor.fetchall()
for col in cols:
    print(f"{col[0]:40s} | {col[1]:30s} | Null: {col[2]:3s} | Key: {col[3]}")

print("\n--- Beispieldaten (erste 5) ---")
cursor.execute("SELECT id, vorname, nachname FROM t_personen LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, {row[1]} {row[2]}")

conn.close()
