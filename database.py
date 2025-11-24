
import sqlite3
from typing import Optional, Tuple, Any

# ----------------------------- #
#  Database Utility Functions   #
# ----------------------------- #

def open_db() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Opens a connection to the local road database.
    Returns both the connection and cursor objects.
    """
    connection = sqlite3.connect("road.db")
    cursor = connection.cursor()
    return connection, cursor


def close_db(connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    """
    Safely closes the cursor and commits pending changes.
    """
    cursor.close()
    connection.commit()
    connection.close()


# ----------------------------- #
#  Schema Creation              #
# ----------------------------- #

def initialize_database():
    """
    Creates the table structure for storing road details
    if it does not already exist.
    """
    conn, cur = open_db()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS road (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            green_time INTEGER,
            vehicle_count INTEGER,
            capacity INTEGER,
            total_time INTEGER,
            hasEmergencyVehicle BOOLEAN,
            filePath TEXT
        )
    """)

    close_db(conn, cur)


# ----------------------------- #
#  Insert Operations            #
# ----------------------------- #

def insert_road(name: str, green: int, count: int, capacity: int,
                total: int, emergency: bool,
                file_path: Optional[str] = None) -> int:
    """
    Inserts a new row into the road table.
    Returns the auto-generated ID of the newly added row.
    """
    conn, cur = open_db()

    cur.execute(
        """INSERT INTO road (name, green_time, vehicle_count, capacity, total_time, 
                             hasEmergencyVehicle, filePath)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (name, green, count, capacity, total, emergency, file_path)
    )

    new_id = cur.lastrowid
    close_db(conn, cur)
    return new_id


# ----------------------------- #
#  General Update Helper        #
# ----------------------------- #

def _update_field(road_id: int, field: str, value: Any):
    """Internal helper to update any single column."""
    conn, cur = open_db()

    query = f"UPDATE road SET {field} = ? WHERE id = ?"
    cur.execute(query, (value, road_id))

    close_db(conn, cur)


# ----------------------------- #
#  Update Methods               #
# ----------------------------- #

def update_green_time(road_id: int, green: int):
    _update_field(road_id, "green_time", green)

def update_vehicle_count(road_id_
