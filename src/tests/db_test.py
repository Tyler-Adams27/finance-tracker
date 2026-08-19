"""
CI Tests for database operations
"""

import sqlite3
import shutil
import unittest
import os
import tempfile
from src.expense import Expense
# Import all DAO functions needed for testing
from src.db import (
    add_expense,
    get_expenses_by_id,
    get_all_expenses,
    update_expense,
    delete_expense,
)


class TestDB(unittest.TestCase):
    """
    Unittest class for testing database operations (CRUD).
    """
    def setUp(self):
        """
        Setup: Creates a unique temporary database file and initializes the schema.
        """
        # Create a unique temporary directory to hold the test database file.
        self.test_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.test_dir, "test_expenses.db")

        # Initialize the database schema directly in this test database
        from src.constants import DB_SCHEMA
        try:
            with sqlite3.connect(self.test_db) as conn:
                cur = conn.cursor()
                cur.execute(DB_SCHEMA)
                conn.commit()
        except sqlite3.Error as e:
            self.fail(f"SQLite3 Error during setup: {e}")

    def tearDown(self):
        """
        Teardown: Ensures the temporary database directory is cleaned up.
        """
        # Remove the temporary directory and all its contents.
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_adding_expense(self):
        """Tests adding a single expense record."""
        self_expense = Expense("10.00", "Food", "McDonalds", "12/08/2026")
        # Use the shared temp file for both setup and testing connections
        added_id = add_expense(self_expense, db_path=self.test_db)
        with sqlite3.connect(self.test_db) as verify_conn:
            cursor = verify_conn.cursor()
            cursor.execute("SELECT amount FROM expenses WHERE id=?", (added_id,))
            row = cursor.fetchone()

        self.assertIsNotNone(added_id, "add_expense should return a valid ID.")
        self.assertIsNotNone(row, "Database should contain the inserted row.")
        self.assertEqual(row[0], "10.00")


    def test_getting_all_expenses(self):
        """Tests fetching all expense records."""
        # Setup: Add multiple expenses
        added_id1 = add_expense(Expense("50.00", "Rent", "Monthly rent payment", "01/08/2026"), db_path=self.test_db)
        added_id2 = add_expense(Expense("5.99", "Food", "Coffee shop", "13/08/2026"), db_path=self.test_db)

        # We'll get the IDs back and verify them

        # Action: Get all expenses
        expenses = get_all_expenses(db_path=self.test_db)

        # Assertion
        self.assertEqual(len(expenses), 2, "Should retrieve exactly two expenses.")
        # Check if the latest (highest ID, added last) is first (due to ORDER BY id DESC)
        self.assertEqual(expenses[0].amount, "5.99")
        self.assertEqual(expenses[1].amount, "50.00")

    def test_get_single_expense_by_id(self):
        """Tests retrieving a single expense record by ID."""
        # Setup: Add an expense we can retrieve by ID (ID 1)
        added_id = add_expense(Expense("25.00", "Transport", "Bus fare", "14/08/2026"), db_path=self.test_db)

        # Action: Use the actual ID returned from setup for reliable testing.
        retrieved = get_expenses_by_id(db_path=self.test_db, expense_id=added_id)

        # Assertion
        self.assertIsNotNone(retrieved, "Should retrieve an existing expense.")
        self.assertEqual(retrieved.amount, "25.00")
        self.assertEqual(retrieved.category, "Transport")

    def test_nonexistent_expense(self):
        """Tests behavior when retrieving a non-existent expense ID."""
        # Action: Try to retrieve an ID that definitely does not exist (e.g., 999)
        retrieved = get_expenses_by_id(db_path=self.test_db, expense_id=999)

        # Assertion
        self.assertIsNone(retrieved, "Should return None for non-existent expense IDs.")

    def test_update_expense(self):
        """Tests updating an existing expense record."""
        # Setup: Add initial expense (ID 1)
        initial_exp = Expense("20.00", "Food", "Initial Lunch", "10/08/2026")
        initial_exp.id = add_expense(initial_exp, db_path=self.test_db)

        # Action: Update fields
        new_amount = "35.50"
        new_category = "Dining Out"
        new_description = "Updated lunch description"
        new_date = "15/08/2026"

        success = update_expense(
            expense_id=initial_exp.id,
            amount=new_amount,
            category=new_category,
            description=new_description,
            date=new_date,
            db_path=self.test_db
        )

        # Verification: Check success and then verify the changes via DB query
        self.assertTrue(success, "update_expense should return True on successful update.")
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT amount, category, description, date FROM expenses WHERE id=?", (initial_exp.id,))
            row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], new_amount)
        self.assertEqual(row[1], new_category)
        self.assertEqual(row[2], new_description)
        self.assertEqual(row[3], new_date)

    def test_delete_expense(self):
        """Tests deleting an expense record."""
        # Setup: Add initial expense (ID 1)
        exp = Expense("75.00", "Travel", "Train ticket", "16/08/2026")
        exp.id = add_expense(exp, db_path=self.test_db)

        # Action: Delete the record by ID 1
        success = delete_expense(db_path=self.test_db, expense_id=exp.id)

        # Verification 1: Check if deletion was reported as successful
        self.assertTrue(success, "delete_expense should return True on successful deletion.")

        # Verification 2: Check if the record actually exists in the database
        with sqlite3.connect(self.test_db) as verify_conn:
            cursor = verify_conn.cursor()
            cursor.execute("SELECT id FROM expenses WHERE id=?", (exp.id,))
            row = cursor.fetchone()

        self.assertIsNone(row, "The expense record should no longer exist after deletion.")


if __name__ == "__main__":
    unittest.main()