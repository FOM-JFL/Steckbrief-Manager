"""Fügt die Spalte it_unterstuetzung zur Tabelle t_hochschulsteckbriefe hinzu."""
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

c.execute("SHOW COLUMNS FROM t_hochschulsteckbriefe LIKE 'it_unterstuetzung'")
if c.fetchall():
    print("Spalte it_unterstuetzung existiert bereits.")
else:
    c.execute("ALTER TABLE t_hochschulsteckbriefe ADD COLUMN it_unterstuetzung TEXT DEFAULT NULL AFTER projektteam")
    conn.commit()
    print("Spalte it_unterstuetzung erfolgreich angelegt.")

conn.close()
