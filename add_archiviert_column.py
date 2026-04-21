"""Fügt die Spalte archiviert zur Tabelle t_hochschulsteckbriefe hinzu."""
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

cursor.execute("SHOW COLUMNS FROM t_hochschulsteckbriefe LIKE 'archiviert'")
if cursor.fetchone():
    print("Spalte archiviert existiert bereits.")
else:
    cursor.execute("ALTER TABLE t_hochschulsteckbriefe ADD COLUMN archiviert TINYINT(1) DEFAULT 0")
    conn.commit()
    print("Spalte archiviert erfolgreich angelegt.")

conn.close()
