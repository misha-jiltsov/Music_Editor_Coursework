import sqlite3
from datetime import datetime
import os

class Database_Manager:
    def __init__(self):
        self.conn = sqlite3.connect("main_database.db") # connect or create the database file
        self.cursor = self.conn.cursor() # create a "cursor" which will interact with the database
        self.create_table() # make sure that the table is created when initialised

    def create_table(self):
        # creates a table which store the filename, the date it was created/updated and its corresponding filepath
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,    
                filename TEXT UNIQUE NOT NULL,
                date_created TEXT NOT NULL,
                filepath TEXT NOT NULL
            )
            """)

        self.conn.commit() # commits changes to the database

    def update_data(self, filename, filepath):
        # updates values in the table or creates a new record is there is no filename of the same name
        self.cursor.execute("""
        INSERT INTO saved_files (filename, date_created, filepath) 
        VALUES (?, ?, ?)
        ON CONFLICT(filename) DO UPDATE SET date_created = excluded.date_created
        """,
(filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filepath)) # passes in all the parameters from the method

        self.conn.commit() # commits changes to database

    def get_recent_tracks(self, amount):
        # returns a list of a user specified amount of the most recent files
        self.cursor.execute("""
        SELECT filename, date_created FROM saved_files
        ORDER BY date_created DESC
        LIMIT ?
        """,
(amount,))
        return self.cursor.fetchall() # returns all files matching criteria

    def get_path_from_name(self, filename):
        # returns the filepath from the filename
        self.cursor.execute("""
                SELECT filepath FROM saved_files
                WHERE filename = ?
                """, (filename,))

        return self.cursor.fetchall() # returns value found

    def check_files_exists_remove_missing(self):
        # selects all ids and filepaths from the table
        self.cursor.execute("""
                SELECT id, filepath FROM saved_files
                """)
        data = self.cursor.fetchall()

        for file in data:
            if not os.path.exists(file[1]): # checks if file still exists
                self.cursor.execute("""
                DELETE FROM saved_files WHERE id = ?;
                """, (file[0],)) # removes file if missing

        self.conn.commit() # commits to database

    def close_connection(self):
        self.conn.close() # closes the connection to the database
