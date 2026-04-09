import mysql.connector, json
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.environ['DB_NAME']
)
cursor = conn.cursor(dictionary=True)

# Aktuellen Wert
cursor.execute("SELECT projektteam FROM t_hochschulsteckbriefe WHERE id = 143")
row = cursor.fetchone()
print(f"Aktuell in DB: {repr(row['projektteam'])}")

# Was sendet das Frontend wenn alle Tags entfernt?
team_empty = json.dumps([])  # "[]"
print(f"JSON.stringify([]): {repr(team_empty)}")

# Simuliere API save Logik
val = team_empty
if val == '' or val is None:
    print("API wuerde None speichern")
else:
    print(f"API wuerde speichern: {repr(val)}")

conn.close()
