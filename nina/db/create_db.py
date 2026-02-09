import sqlite3
import json
import os

def create_database():
    # Pfad zur DB im selben Verzeichnis wie dieses Skript
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'levels.db')
    
    # Verbindung herstellen (erstellt die Datei, wenn sie nicht existiert)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabelle erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            map_data TEXT NOT NULL
        )
    ''')
    
    # Beispiel-Level Daten
    level_1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    level_2 = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    # Daten einfügen
    levels_to_insert = [
        ("Level 1", json.dumps(level_1)),
        ("Level 2", json.dumps(level_2))
    ]
    
    for name, data in levels_to_insert:
        try:
            cursor.execute("INSERT INTO levels (name, map_data) VALUES (?, ?)", (name, data))
            print(f"{name} wurde hinzugefügt.")
        except sqlite3.IntegrityError:
            print(f"{name} existiert bereits.")
            
    conn.commit()
    conn.close()
    print(f"Datenbank erfolgreich erstellt unter: {db_path}")

if __name__ == "__main__":
    create_database()
