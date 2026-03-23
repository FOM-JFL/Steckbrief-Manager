"""Erstellt die Benutzer-Tabelle für das Rechtesystem"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.environ.get('DB_NAME', 'bcw_allgemein'),
    ssl_disabled=False
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS t_steckbrief_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        display_name VARCHAR(200),
        email VARCHAR(200),
        role ENUM('viewer', 'editor', 'admin') NOT NULL DEFAULT 'viewer',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_login DATETIME
    )
""")
conn.commit()
print('Tabelle t_steckbrief_users angelegt/existiert bereits.')

cursor.execute('DESCRIBE t_steckbrief_users')
for row in cursor.fetchall():
    print(f'  {row[0]:20s} {row[1]}')

conn.close()
