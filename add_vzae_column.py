"""Fügt die Spalte nutzen_vzae zur Tabelle t_hochschulsteckbriefe hinzu."""
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

# Prüfen ob Spalte existiert
c.execute("SHOW COLUMNS FROM t_hochschulsteckbriefe LIKE 'nutzen_vzae'")
if c.fetchall():
    print("Spalte nutzen_vzae existiert bereits.")
else:
    c.execute("ALTER TABLE t_hochschulsteckbriefe ADD COLUMN nutzen_vzae VARCHAR(255) DEFAULT NULL AFTER nutzen_qualitaet_text")
    conn.commit()
    print("Spalte nutzen_vzae erfolgreich angelegt.")

conn.close()
