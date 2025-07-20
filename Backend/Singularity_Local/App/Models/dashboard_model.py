from datetime import datetime

from Backend.Singularity_Local.App.Utils.config_helper import load_config
from Backend.Singularity_Local.App.Utils.local_db import get_db_connection

def get_rooms(house_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT * FROM Room WHERE HouseID = ? ORDER BY CreatedAt ASC",
        (house_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def create_room(house_id, room_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.utcnow().isoformat()

    cursor.execute(
        "INSERT INTO Room (HouseID, RoomName, CreatedAt) VALUES (?, ?, ?)",
        (house_id, room_name, created_at)
    )
    room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return room_id

def update_room(room_id, room_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Room SET RoomName = ? WHERE RoomID = ?",
        (room_name, room_id)
    )
    conn.commit()
    conn.close()

def delete_room(room_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Room WHERE RoomID = ?", (room_id,))
    conn.commit()
    conn.close()


def get_house_from_config(house_id):
    config = load_config()
    if not config:
        return None

    if str(config.get("house_id")) != str(house_id):
        return None

    return {
        "HouseName": config.get("house_name"),
        "City": config.get("city"),
        "Street": config.get("street"),
        "PostalCode": config.get("postal_code"),
        "Country": config.get("country"),
        "CountryCode": config.get("country_code")
    }