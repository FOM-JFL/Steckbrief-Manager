import mysql.connector, os
from dotenv import load_dotenv
load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
)
cur = conn.cursor(dictionary=True)

# API-Suche simulieren (gleiche Query wie api_server.py)
q = 'Koch'
cur.execute(
    """SELECT DISTINCT p.PersonenID, p.Vorname, p.Nachname, p.Titel_de
       FROM datapool.t_personen p
       INNER JOIN tele_v.t_lohnmandanten lm ON lm.PersonenFID = p.PersonenID
           AND lm.Start <= CURDATE()
           AND (lm.End IS NULL OR lm.End >= CURDATE())
           AND lm.Deaktiviert = 0
       WHERE (p.Nachname LIKE %s OR p.Vorname LIKE %s) AND p.Deaktiviert='N'
       ORDER BY p.Nachname, p.Vorname LIMIT 20""",
    (f'%{q}%', f'%{q}%')
)
results = cur.fetchall()
print(f'API-Suche fuer "{q}" ({len(results)} Treffer):')
for r in results:
    print(f"  {r['PersonenID']}: {r['Titel_de']} {r['Vorname']} {r['Nachname']}")

conn.close()
