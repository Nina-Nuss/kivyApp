import sqlite3
import json
import os


def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "levels.db")


def create_database():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ── Level-Tabelle ──────────────────────────────────────────
    # Zellentypen:
    #   0 = freier Weg
    #   1 = Wand
    #   2 = Loch (Falle) → Kugel fällt, Neustart
    #   3 = Ziel          → Level gewonnen
    #   4 = Start-Position der Kugel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    UNIQUE NOT NULL,
            map_data  TEXT    NOT NULL
        )
    ''')

    # ── Fortschritts-Tabelle ───────────────────────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_progress (
            level_name TEXT    PRIMARY KEY,
            unlocked   INTEGER DEFAULT 0
        )
    ''')

    # ── Level-Daten ────────────────────────────────────────────
    # Legende: 0=Weg, 1=Wand, 2=Loch, 3=Ziel, 4=Start
    level_1 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 4, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 2, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 2, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 2, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    level_2 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 4, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 2, 1, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 2, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 2, 1, 0, 0, 0, 1, 2, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    level_3 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 4, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1],
        [1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
        [1, 2, 0, 0, 0, 2, 1, 2, 0, 0, 0, 2, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 2, 0, 0, 0, 0, 0, 2, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    levels_data = [
        ("Level 1", level_1),
        ("Level 2", level_2),
        ("Level 3", level_3),
    ]

    for name, grid in levels_data:
        try:
            cursor.execute(
                "INSERT INTO levels (name, map_data) VALUES (?, ?)",
                (name, json.dumps(grid))
            )
            print(f"  ✓ {name} eingefügt")
        except sqlite3.IntegrityError:
            print(f"  – {name} existiert bereits")

    # ── Fortschritt initialisieren ─────────────────────────────
    for name, _ in levels_data:
        unlocked = 1 if name == "Level 1" else 0
        try:
            cursor.execute(
                "INSERT INTO player_progress (level_name, unlocked) VALUES (?, ?)",
                (name, unlocked)
            )
        except sqlite3.IntegrityError:
            pass  # Bereits vorhanden

    conn.commit()
    conn.close()
    print(f"\nDatenbank bereit: {db_path}")


if __name__ == "__main__":
    create_database()
