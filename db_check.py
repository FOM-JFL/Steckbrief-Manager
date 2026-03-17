import mysql.connector

conn = mysql.connector.connect(
    host='mariadb.bcw-intern.local',
    user='ralf.schmitz',
    password='d-kvsl1715',
    database='bcw_allgemein',
    ssl_disabled=False
)
cursor = conn.cursor()
cursor.execute("SHOW TABLES LIKE '%steckbrief%'")
tables = cursor.fetchall()
if tables:
    for t in tables:
        print(t[0])
else:
    print('Keine Tabellen mit steckbrief gefunden')
conn.close()
