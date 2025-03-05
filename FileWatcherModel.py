from File import FileClass
from DataWarehouse import DataWarehouse
import sqlite3
import time
import threading
from SecurityMonitor import *

class FileModel:
    """Stores and manages file metadata."""
    def __init__(self, db_path="file_watcher_v1.db"):
        self.warehouse = DataWarehouse()  # Optional: Keep in-memory storage
        self.db_path = db_path
        self.local = threading.local()  # Thread-local storage
        self.table_name = None

    def _get_connection(self):
        """Get a database connection for the current thread."""
        if not hasattr(self.local, "connection"):
            self.local.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.local.connection


    def set_table_name(self, name):
        self.table_name = name
        self._initialize_database()

    def set_db_path(self, db_path):
        self.db_path = db_path

    # def update_file(self, file_name, event_type, date, time):
    #     self.warehouse.push(FileClass(file_name, event_type,date,time))

    # def get_all_files(self):
    #     return self.warehouse.peek()

    # def get_file_info(self, file_name):
    #     return self.warehouse.peek()

    def _initialize_database(self):
        """Initialize the database (create tables if they don't exist)."""
        try:
            with self._get_connection() as conn:
                conn.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_name TEXT NOT NULL UNIQUE,
                        event_type TEXT NOT NULL,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL
                    )
                ''')
                print("Database initialized.")
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")

    def update_file(self, file_name, event_type, date, time):
        """Update or insert file metadata into the database."""
        try:
            self.warehouse.push(FileClass(file_name, event_type, date, time))
            with self._get_connection() as conn:
                # Insert or replace file metadata
                conn.execute(f'''INSERT OR REPLACE INTO {self.table_name} (file_name, event_type, date, time)
                    VALUES (?, ?, ?, ?)'''  , (file_name, event_type, date, time))
                print(f"Updated file in database: {file_name} - {event_type}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_all_files(self):
        """Retrieve all file metadata from the database."""
        print(self.table_name)
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                conn.execute(f'''SELECT * FROM {self.table_name}''')
                rows = cursor.fetchall()
                print(rows)
                return [FileClass(row[1], row[2], row[3], row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def get_file_info(self, file_name):
        """Retrieve metadata for a specific file from the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(f'''
                    SELECT * FROM {self.table_name} WHERE file_name = ?
                ''', (file_name,))
                row = cursor.fetchone()
                if row:
                    return FileClass(row[1], row[2], row[3], row[4])
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        if hasattr(self.local, "connection"):
            self.local.connection.close()
            print("Database connection closed.")

    def write_data(self):
        savetime = time.strftime("%Y%m%d%H%M%S")
        tablename = "GuardDogLog_" + savetime
        dbname = tablename + ".db"
        self.set_db_path(dbname)
        self.set_table_name(tablename)


       # self._initialize_database()
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                event_type TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL
                )
            ''')

        for i in range(self.warehouse.size):
            data = self.warehouse.pop()
            cursor.execute(f'''
                INSERT INTO {self.table_name} (filename, event_type, date, time) VALUES (?, ?, ?, ?)
                ''', (data.file_name, data.event_type, data.date, data.time,))

        conn.commit()
        conn.close()


        return dbname


    def alert_security(self, db_file):
        SecurityMonitor





