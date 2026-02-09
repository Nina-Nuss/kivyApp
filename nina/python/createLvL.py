import sys
import os
import json

# Pfad zum Parent-Directory hinzufügen, damit wir 'test' und 'db' finden
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    from test.maze import create_maze
    from db.selectMap import get_level_map # Nur zum Testen
except ImportError as e:
    print(f"Fehler beim Importieren: {e}")
    print("Stelle sicher, dass du das Skript aus dem richtigen Verzeichnis startest.")
    sys.exit(1)

def generate_new_level(width=21, height=11):
    """
    Generiert ein neues Level mithilfe des Maze-Algorithmus.
    """
    print(f"Generiere Maze ({width}x{height})...")
    
    # Maze erstellen (0=Weg, 1=Wand)
    maze_map = create_maze(width, height)
    
    return maze_map

if __name__ == "__main__":
    # 1. Level generieren
    my_level = generate_new_level(21, 11)
    
    # 2. Anzeigen
    print("\nGeneriertes Level:")
    for row in my_level:
        # # für Wand, Leerzeichen für Weg
        print("".join("1" if cell else "0" for cell in row))
    
    # 3. (Optional) Hier könnte man das Level in die Datenbank speichern
    # import sqlite3
    # ... code db insert ...
