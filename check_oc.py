import mysql.connector

# Steckbrief finden
conn = mysql.connector.connect(host='mariadb.bcw-intern.local', user='ralf.schmitz', password='d-kvsl1715', database='bcw_allgemein')
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, titel, anforderungsmanagerFID FROM t_hochschulsteckbriefe WHERE titel LIKE %s", ('%OC%App%',))
for r in cursor.fetchall():
    print("Steckbrief:", r)
conn.close()

# Person suchen
conn2 = mysql.connector.connect(host='mariadb.bcw-intern.local', user='ralf.schmitz', password='d-kvsl1715', database='datapool')
cursor2 = conn2.cursor(dictionary=True)
cursor2.execute("""
    SELECT DISTINCT p.PersonenID, p.Vorname, p.Nachname, p.Titel_de, p.Geschlecht
    FROM t_personen p
    INNER JOIN tele_v.t_lohnmandanten lm ON lm.PersonenFID = p.PersonenID
        AND lm.Start <= CURDATE()
        AND (lm.End IS NULL OR lm.End >= CURDATE())
        AND lm.Deaktiviert = 0
    WHERE (p.Nachname LIKE %s OR p.Nachname LIKE %s) AND p.Deaktiviert='N'
""", ('%eidk%', '%ergel%'))
for r in cursor2.fetchall():
    print("Person:", r)
conn2.close()
