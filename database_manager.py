import sqlite3
from datetime import datetime
import os

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

    def get_path_from_name(self, filename):
        self.cursor.execute("""
                SELECT filepath FROM saved_files
                WHERE filename = ?
                """, (filename,))

        return self.cursor.fetchall()

    def check_files_exists_remove_missing(self):
        self.cursor.execute("""
                SELECT id, filepath FROM saved_files
                """)
        data = self.cursor.fetchall()

        for file in data:
            if not os.path.exists(file[1]):
                self.cursor.execute("""
                DELETE FROM saved_files WHERE id = ?;
                """, (file[0],))

        self.conn.commit()


    def close_connection(self):
        self.conn.close()
