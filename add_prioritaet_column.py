"""Fügt die Spalte prioritaet zur Tabelle t_hochschulsteckbriefe hinzu."""
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

conn = mysql.connector.connect(
    host=os.environ.get('DB_HOST', 'mariadb.bcw-intern.local'),
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.environ.get('DB_NAME', 'bcw_allgemein')
)
c = conn.cursor()

c.execute("SHOW COLUMNS FROM t_hochschulsteckbriefe LIKE 'prioritaet'")
if c.fetchall():
    print("Spalte prioritaet existiert bereits.")
else:
    c.execute("ALTER TABLE t_hochschulsteckbriefe ADD COLUMN prioritaet VARCHAR(10) DEFAULT NULL AFTER prozesscluster")
    conn.commit()
    print("Spalte prioritaet erfolgreich angelegt.")

conn.close()
