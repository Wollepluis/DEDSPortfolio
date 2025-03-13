import sqlite3 as sql
import os

db_folder = "Data"
db_path = os.path.join(db_folder, "database.db")
os.makedirs(db_folder, exist_ok=True)

sql_file = "/home/mark/VSCode/DEDSPortfolio/src/create_database.sql"
conn = sql.connect(db_path)
cursor = conn.cursor()

with open(sql_file, "r") as file:
    sql_script = file.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()

print(f"Database created at {db_path}")