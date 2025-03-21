import sqlite3
from datetime import datetime
class Database_Manager:
    def __init__(self):
        self.conn = sqlite3.connect("main_database.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                date_created TEXT NOT NULL,
                filepath TEXT NOT NULL
            )
            """)
        self.conn.commit()

    def update_data(self, filename, filepath):
        self.cursor.execute("""
        INSERT INTO saved_files (filename, date_created, filepath) 
        VALUES (?, ?, ?)
        ON CONFLICT(filename) DO UPDATE SET date_created = excluded.date_created
        """,
(filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filepath))

        self.conn.commit()

    def get_recent_tracks(self, amount):
        self.cursor.execute("""
        SELECT filename, date_created FROM saved_files
        ORDER BY date_created DESC
        LIMIT ?
        """,
(amount,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

