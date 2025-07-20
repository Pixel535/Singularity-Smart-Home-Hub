import os
import sqlite3
from Backend.Singularity_Local.App.config import Config

DB_PATH = os.path.join(Config.STORAGE_PATH, "local_data.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_local_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Room (
            RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
            HouseID INTEGER NOT NULL,
            RoomName TEXT NOT NULL,
            CreatedAt TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
