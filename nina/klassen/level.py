import json
import os

class Level:
    def __init__(self, level_name):
        self.src = level_name
        self.map = self.load_map(level_name)

    def load_map(self, level_name):
        # Pfad zur JSON-Datei.
        path = os.path.join("db", "/db/levels.json")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Prüfen, ob das Level existiert, sonst leere Liste zurückgeben
            if level_name in data:
                return data[level_name]
            else:
                print(f"Warnung: Level '{level_name}' nicht in {path} gefunden.")
                return []
                
        except FileNotFoundError:
            print(f"Fehler: Datei {path} nicht gefunden.")
            return []

    def get_map(self):
        return self.map
    
    

