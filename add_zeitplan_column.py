"""Add zeitplan_data column to t_hochschulsteckbriefe if it doesn't exist."""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
)
cursor = conn.cursor()

cursor.execute("SHOW COLUMNS FROM t_hochschulsteckbriefe LIKE 'zeitplan_data'")
result = cursor.fetchone()

if result:
    print("Column 'zeitplan_data' already exists.")
else:
    cursor.execute("ALTER TABLE t_hochschulsteckbriefe ADD COLUMN zeitplan_data LONGTEXT NULL")
    conn.commit()
    print("Column 'zeitplan_data' added successfully.")

conn.close()
