import mysql.connector
conn = mysql.connector.connect(host='mariadb.bcw-intern.local', user='ralf.schmitz', password='d-kvsl1715', database='datapool')
cursor = conn.cursor(dictionary=True)
cursor.execute("""
    SELECT DISTINCT p.PersonenID, p.Vorname, p.Nachname, p.Titel_de, p.Geschlecht
    FROM t_personen p
    INNER JOIN tele_v.t_lohnmandanten lm ON lm.PersonenFID = p.PersonenID
        AND lm.Start <= CURDATE()
        AND (lm.End IS NULL OR lm.End >= CURDATE())
        AND lm.Deaktiviert = 0
    WHERE p.Nachname LIKE %s AND p.Deaktiviert='N'
""", ('Dittrich%',))
for r in cursor.fetchall():
    print(r)
conn.close()
