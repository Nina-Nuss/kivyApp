import sqlite3
import os

def delete_level(level_name):
    """Löscht ein Level anhand des Namens aus der Datenbank."""
    # Pfad zur DB relativ zum Skript
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'levels.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM levels WHERE name = ?", (level_name,))
        if cursor.rowcount > 0:
            print(f"Level '{level_name}' wurde erfolgreich gelöscht.")
        else:
            print(f"Level '{level_name}' wurde nicht gefunden.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        conn.close()

def delete_all_levels():
    """Löscht ALLE Level aus der Datenbank."""
    # Pfad zur DB relativ zum Skript
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'levels.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM levels")
        print(f"Alle Level wurden gelöscht. ({cursor.rowcount} Einträge entfernt)")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== Level Loesch-Tool ===")
    print("1. Einzelnes Level loeschen")
    print("2. Alle Level löschen")
    
    choice = input("Bitte wählen (1 oder 2): ")

    if choice == "1":
        name = input("Geben Sie den Namen des Levels ein (z.B. 'Level 1'): ")
        delete_level(name)
    elif choice == "2":
        confirm = input("ACHTUNG: Alle Daten werden gelöscht! Fortfahren? (j/n): ")
        if confirm.lower() == 'j':
            delete_all_levels()
        else:
            print("Abgebrochen.")
    else:
        print("Ungültige Eingabe.")
