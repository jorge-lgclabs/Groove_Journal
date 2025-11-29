import unittest

from app import create_app
from app.models import insert_new_album
from app.services.db_connection import get_connection


class TestInsertAlbumProcedure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create the Flask app and activate the application context
        cls.app = create_app()  # Ensure your app factory is properly configured
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        cls.conn = get_connection()
        if cls.conn is None:
            raise RuntimeError("Failed to establish a database connection.")
        cls.cursor = cls.conn.cursor()
        if cls.cursor is None:
            raise RuntimeError("Failed to create a database cursor.")

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute("CALL sp_ResetInitialData")
        cls.conn.commit()
        cls.cursor.close()
        cls.conn.close()

    def setUp(self):
        self.cursor.execute("CALL sp_ResetInitialData")
        if self.conn:
            self.conn.commit()

    def test_add_album(self):
        album_entry_title = "Test Album"
        album_entry_label = "Test Label"
        album_entry_country = "Test Country"
        album_entry_year = 2023

        result = insert_new_album(
            album_entry_title,
            album_entry_label,
            album_entry_country,
            album_entry_year,
        )

        # Verify the result
        self.assertIsNotNone(result, "The procedure did not return an album ID.")
        self.assertGreater(result, 0, "The returned album ID should be greater than 0.")

        # Verify the album was inserted into the database
        self.cursor.execute("SELECT * FROM albums WHERE album_id = %s", (result,))
        album = self.cursor.fetchone()
        self.assertIsNotNone(album, "The album was not inserted into the database.")
        self.assertIsInstance(album, tuple, "The fetched album should be a tuple.")
        self.assertEqual(album[1], album_entry_title, "The album title does not match.")
        self.assertEqual(album[2], album_entry_label, "The album label does not match.")
        self.assertEqual(
            album[3], album_entry_country, "The album country does not match."
        )
        self.assertEqual(album[4], album_entry_year, "The album year does not match.")


if __name__ == "__main__":
    unittest.main()
