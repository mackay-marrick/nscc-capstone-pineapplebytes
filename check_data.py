import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"

conn = pyodbc.connect(conn_str)
cur = conn.cursor()

# Check company count
cur.execute("SELECT COUNT(*) FROM company")
count = cur.fetchone()[0]
print(f"Company count: {count}")

# List first 10 company IDs
cur.execute("SELECT company_id, company_name FROM company ORDER BY company_id")
rows = cur.fetchall()
for row in rows[:10]:
    print(f"Company ID: {row[0]}, Name: {row[1]}")

conn.close()