import sqlite3
import json
import os

# Pfad zur DB
base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, "levels.db")
conn = sqlite3.connect(path)
cursor = conn.cursor()

# Level laden
cursor.execute("SELECT map_data FROM levels WHERE name = ?", ("Level 1",))
row = cursor.fetchone()

def get_levels_from_db():
    if row:
        level_map = json.loads(row[0])
        print(level_map)

conn.close()