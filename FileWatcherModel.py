from File import FileClass
from DataWarehouse import DataWarehouse
import sqlite3
import time

class FileModel:
    """Stores and manages file metadata."""
    def __init__(self):
        self.warehouse = DataWarehouse()  # Dictionary to store metadata

    def update_file(self, path, event_type, date, time):
        self.warehouse.push(FileClass(path, event_type,date,time))

    def get_all_files(self):
        return self.warehouse.peek()

    def get_file_info(self, path):
        return self.warehouse.peek()

    def write_data(self):
        savetime = time.strftime("%Y%m%d%H%M%S")
        tablename = "GuardDogLog_" + savetime
        dbname = tablename + ".db"
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {tablename} (
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
                INSERT INTO {tablename} (filename, event_type, date, time) VALUES (?, ?, ?, ?)
                ''', (data.path, data.event_type, data.date, data.time,))

        conn.commit()
        conn.close()


        return dbname


