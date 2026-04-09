import mysql.connector

conn = mysql.connector.connect(
    host='mariadb.bcw-intern.local',
    user='ralf.schmitz',
    password='d-kvsl1715',
    database='bcw_allgemein',
    charset='utf8mb4'
)
cur = conn.cursor()
cur.execute("""
    SELECT id, titel, prozessverantwortlicherFID
    FROM t_hochschulsteckbriefe 
    WHERE titel LIKE '%KI Pilot%' OR titel LIKE '%Chatbot%'
""")
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
print("Columns:", cols)
for r in rows:
    for c, v in zip(cols, r):
        print(f"  {c}: {v}")
conn.close()
