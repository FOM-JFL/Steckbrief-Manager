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

# 1. Was steht aktuell in der DB fuer Steckbrief 53?
cur.execute('SELECT id, titel, prozessverantwortlicherFID FROM t_hochschulsteckbriefe WHERE id=53')
row = cur.fetchone()
print('=== Steckbrief 53 ===')
print(row)

# 2. Gibt es Hittinger in t_personen?
cur.execute(
    'SELECT PersonenID, Vorname, Nachname, Titel_de FROM datapool.t_personen WHERE Nachname LIKE %s AND Deaktiviert=%s',
    ('%Hittinger%', 'N')
)
personen = cur.fetchall()
print('\n=== Personen Hittinger ===')
for p in personen:
    print(p)

# 3. Prüfe auch, was die Personen-Suche API liefern würde (gleiche Query wie api_server.py)
q = 'Hittinger'
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
api_results = cur.fetchall()
print(f'\n=== API-Suche fuer "{q}" ===')
for r in api_results:
    print(r)
print(f'Anzahl Treffer: {len(api_results)}')

conn.close()
