import sqlite3
import json
import os

def get_level_map(level_name):
    """
    Holt die Map-Daten für ein bestimmtes Level aus der Datenbank.
    Gibt eine Liste von Listen zurück oder None, wenn das Level nicht gefunden wurde.
    """
    # Pfad zur DB relativ zum Skript
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "levels.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT map_data FROM levels WHERE name = ?", (level_name,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            # JSON-String zurück in Python-Liste umwandeln
            return json.loads(row[0])
        else:
            print(f"Level '{level_name}' nicht gefunden.")
            return None
            
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        return None







