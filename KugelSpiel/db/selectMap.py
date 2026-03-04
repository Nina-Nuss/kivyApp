import sqlite3
import json
import os


def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "levels.db")


def get_level_map(level_name):
    """Gibt das 2D-Grid eines Levels zurück."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT map_data FROM levels WHERE name = ?", (level_name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
        print(f"Level '{level_name}' nicht gefunden.")
        return None
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        return None


def get_all_levels():
    """Gibt alle Level-Namen mit Unlock-Status zurück.
    Rückgabe: Liste von (name, unlocked) Tupeln."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute('''
            SELECT l.name, COALESCE(p.unlocked, 0)
            FROM levels l
            LEFT JOIN player_progress p ON l.name = p.level_name
            ORDER BY l.id
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows  # [(name, unlocked), ...]
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        return []


def unlock_level(level_name):
    """Schaltet ein Level frei."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO player_progress (level_name, unlocked)
            VALUES (?, 1)
            ON CONFLICT(level_name) DO UPDATE SET unlocked = 1
        ''', (level_name,))
        conn.commit()
        conn.close()
        print(f"Level '{level_name}' freigeschaltet.")
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")


def get_next_level_name(current_level_name):
    """Gibt den Namen des nächsten Levels zurück oder None."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM levels WHERE name = ?", (current_level_name,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        current_id = row[0]
        cursor.execute("SELECT name FROM levels WHERE id = ?", (current_id + 1,))
        next_row = cursor.fetchone()
        conn.close()
        return next_row[0] if next_row else None
    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")
        return None


def find_start_position(grid):
    """Sucht die Startposition (Zelltyp 4) im Grid.
    Gibt (col, row) zurück, oder (1, 1) als Fallback."""
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == 4:
                return col_idx, row_idx
    return 1, 1
