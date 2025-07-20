from Backend.Singularity_Local.App.Utils.local_db import get_db_connection

def get_room_by_id(room_id: int) -> dict | None:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Room WHERE RoomID = ?", (room_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)
