import SecurityMonitor
from File import FileClass
from DataWarehouse import DataWarehouse
import sqlite3
import time
import threading
from SecurityMonitor import *
import zipfile

class FileModel:
    """Stores and manages file metadata."""
    def __init__(self, db_path="file_watcher_v1.db"):
        self._warehouse = DataWarehouse()  # Optional: Keep in-memory storage
        self._db_path = db_path
        self._local = threading.local()  # Thread-local storage
        self._table_name = None
        self._initialize_database()

    def _get_connection(self):
        """Get a database connection for the current thread."""
        if not hasattr(self._local, "connection"):
            self._local.connection = sqlite3.connect(self._db_path, check_same_thread=False)
        return self._local.connection


    def set_table_name(self, name):
        self._table_name = name


    def set_db_path(self, db_path):
        self._db_path = db_path

    def _initialize_database(self):
        """Initialize the database (create tables if they don't exist)."""
        try:
            with self._get_connection() as conn:
                conn.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self._table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_name TEXT NOT NULL UNIQUE,
                        file_extension TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL
                    )
                ''')
                print("Database initialized.")
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")

    def update_file(self, file_name, file_extension, event_type, date, time):
        """Update or insert file metadata into the database."""
        try:
            self._warehouse.push(FileClass(file_name, file_extension, event_type, date, time))
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_all_files(self):
        """Retrieve all file metadata from the database."""
        print(self._table_name)
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Fetch all table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = cursor.fetchall()

                all_records = []

                for table in tables:
                    table_name = table[0]
                    print(f"Fetching data from table: {table_name}")

                    cursor.execute(f"PRAGMA table_info({table_name})")  # Get column count
                    columns = cursor.fetchall()
                    column_count = len(columns)

                    cursor.execute(f'''SELECT * FROM {table_name}''')
                    rows = cursor.fetchall()
                    print(rows)

                    # Convert rows into FileClass objects
                    for row in rows:
                        if column_count >= 6:
                            print(row[5])
                            all_records.append(FileClass(row[1], row[2], row[3], row[4], row[5]))
                return all_records
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def get_file_info(self, file_name):
        """Retrieve metadata for a specific file from the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(f'''
                    SELECT * FROM {self._table_name} WHERE filename = ?
                ''', (file_name,))
                row = cursor.fetchone()
                print(row)
                if row:
                    return FileClass(row[1], row[2], row[3], row[4])
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        if hasattr(self._local, "connection"):
            self._local.connection.close()
            print("Database connection closed.")

    def write_data(self):
        savetime = time.strftime("%Y%m%d%H%M%S")
        tablename = "GuardDogLog_" + savetime
        self.set_table_name(tablename)


       # self._initialize_database()
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()

        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self._table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_extension TEXT NOT NULL,
                event_type TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL
                )
            ''')

        for i in range(self._warehouse._size):
            data = self._warehouse.pop()
            cursor.execute(f'''
                INSERT INTO {self._table_name} (filename, file_extension, event_type, date, time) VALUES (?, ?, ?, ?, ?)
                ''', (data.file_name, data.file_extension, data.event_type, data.date, data.time,))

        conn.commit()
        conn.close()


        return self._db_path


    def alert_security(self, db_file):
        db_base = db_file.split('.')[0]
        zip_db = zipfile.ZipFile(f'{db_base}.zip', mode='w').write(db_file)
        security = SecurityMonitor(db_file=f'{db_base}.zip')
        security.send_email()





