"""Fügt die Spalte phasen_data zur Tabelle t_hochschulsteckbriefe hinzu."""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.environ.get('DB_HOST', 'mariadb.bcw-intern.local'),
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.environ.get('DB_NAME', 'bcw_allgemein'),
    ssl_disabled=False
)
cursor = conn.cursor()

# Prüfen ob Spalte existiert
cursor.execute("SHOW COLUMNS FROM t_hochschulsteckbriefe LIKE 'phasen_data'")
if cursor.fetchone():
    print("Spalte phasen_data existiert bereits.")
else:
    cursor.execute("ALTER TABLE t_hochschulsteckbriefe ADD COLUMN phasen_data LONGTEXT DEFAULT NULL")
    conn.commit()
    print("Spalte phasen_data erfolgreich angelegt.")

conn.close()
