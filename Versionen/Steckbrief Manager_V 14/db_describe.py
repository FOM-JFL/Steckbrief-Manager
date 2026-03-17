import mysql.connector

conn = mysql.connector.connect(
    host='mariadb.bcw-intern.local',
    user='ralf.schmitz',
    password='d-kvsl1715',
    database='bcw_allgemein',
    ssl_disabled=False
)
cursor = conn.cursor()
cursor.execute("DESCRIBE t_hochschulsteckbriefe")
cols = cursor.fetchall()
for col in cols:
    print(f"{col[0]:40s} | {col[1]:30s} | Null: {col[2]:3s} | Key: {col[3]:3s} | Default: {col[4]}")
conn.close()
