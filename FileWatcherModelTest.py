import unittest
import sqlite3
from File import FileClass
from DataWarehouse import DataWarehouse
from FileWatcherModel import FileModel  # Assuming the FileModel is in FileModel.py


class TestFileModel(unittest.TestCase):

    def setUp(self):
        self.model = FileModel()
        self.model._initialize_database()  # Create the table

    def test_update_file(self):
        """Test inserting a file record into the in-memory database and committing to SQLite."""
        self.model.update_file("test.txt", ".txt", "created", "2025-03-10", "12:30:00")  # Add to in-memory DB

        self.model.write_data()

        # Fetch from database
        conn = self.model._get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {self.model.table_name}")
        rows = cursor.fetchall()
        print("Database content after write_data():", rows)  # Debugging

        cursor.execute(f"SELECT * FROM {self.model.table_name} WHERE filename = ?", ("test.txt",))
        row = cursor.fetchone()

        self.assertIsNotNone(row)  # Ensure a record was inserted
        self.assertEqual(row[1], "test.txt")  # Check filename
        self.assertEqual(row[2], ".txt")  # Check file extension
        self.assertEqual(row[3], "created")  # Check event type

    def test_get_file_info(self):
        """Test retrieving metadata for a specific file."""
        self.model.update_file("example.docx", ".docx", "modified", "2025-03-11", "14:45:00")
        self.model.write_data()
        file_info = self.model.get_file_info("example.docx")


        self.assertIsNotNone(file_info)
        self.assertEqual(file_info.file_name, "example.docx")
        self.assertEqual(file_info.file_extension, ".docx")
        self.assertEqual(file_info.event_type, "modified")

    def test_get_all_files(self):
        """Test retrieving all file records from multiple tables."""
        self.model.update_file("file1.pdf", ".pdf", "deleted", "2025-03-12", "09:15:00")
        self.model.update_file("file2.png", ".png", "modified", "2025-03-12", "10:00:00")
        self.model.write_data()
        all_files = self.model.get_all_files()
        self.assertGreaterEqual(len(all_files), 2)  # Ensure at least 2 records exist

    def test_get_file_info_nonexistent(self):
        """Test retrieving a file that does not exist."""
        file_info = self.model.get_file_info("nonexistent.txt")
        self.assertIsNone(file_info)  # Should return None for nonexistent file

    def test_database_error_handling(self):
        """Test handling of database errors gracefully."""
        self.model.table_name = "nonexistent_table"  # Set a wrong table name
        file_info = self.model.get_file_info("test.txt")
        self.assertIsNone(file_info)  # Should not crash, should return None

    def test_write_data(self):
        """Test writing stored warehouse data to the database."""
        self.model.warehouse.push(FileClass("stored.log", ".log", "created", "2025-03-13", "11:00:00"))
        db_file = self.model.write_data()

        # Ensure data was written
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.model.table_name} WHERE filename = ?", ("stored.log",))
        row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[1], "stored.log")
        conn.close()

    def tearDown(self):
        """Close database connection after each test."""
        self.model.close_connection()


# Run the unit tests
if __name__ == "__main__":
    unittest.main()
