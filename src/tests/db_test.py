"""
CI Tests for database operations
"""

import sqlite3
import unittest
import os
from src.expense import Expense
from src.db import add_expense
from src.constants import DB_SCHEMA

class TestDB(unittest.TestCase):
    """
    Unittest class for testing database operations.
    """
    def setUp(self):
        """
        The "setup" stage of the test
        """
        # Ensures absolute path is correct
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_db = os.path.join(script_dir, ".", "tests.db")

        if os.path.exists(self.test_db):
            os.remove(self.test_db)

        with sqlite3.connect(self.test_db) as conn:
            cur = conn.cursor()
            cur.execute(DB_SCHEMA)
            conn.commit()

    def tearDown(self):
        """
        The "end" stage of the test
        """
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_adding_expense(self):
        """
        The actual test case
        """
        self_expense = Expense("10.00", "Food", "McDonalds", "12/08/2026")
        add_expense(self_expense, self.test_db)
        with sqlite3.connect(self.test_db) as verify_conn:
            cursor = verify_conn.cursor()
            cursor.execute("SELECT amount FROM expenses")
            row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "10.00")

if __name__ == "__main__":
    unittest.main()
