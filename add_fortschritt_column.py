"""
Migration: Spalte 'fortschritt' (INT, 0-100) zur Tabelle t_hochschulsteckbriefe hinzufügen.
"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'mariadb.bcw-intern.local'),
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.getenv('DB_NAME', 'bcw_allgemein'),
    ssl_disabled=False
)
cursor = conn.cursor()

# Prüfen ob Spalte existiert
cursor.execute("""
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 't_hochschulsteckbriefe' AND COLUMN_NAME = 'fortschritt'
""", (os.getenv('DB_NAME'),))

if cursor.fetchone()[0] == 0:
    print("Spalte 'fortschritt' wird hinzugefügt...")
    cursor.execute("ALTER TABLE t_hochschulsteckbriefe ADD COLUMN fortschritt INT DEFAULT 0 AFTER gesamtstatus")
    conn.commit()
    print("Fertig.")
else:
    print("Spalte 'fortschritt' existiert bereits.")

cursor.close()
conn.close()
