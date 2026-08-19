"""
Data Access Object (DAO) for Expenses.

Handles all low-level database interactions using SQLite. It abstracts 
the complexity of connection management and transaction execution from the rest of the application.
All functions here cause side effects by writing to or reading from 'expenses.db'.
"""
import os
import sqlite3
from src.expense import Expense
from src.constants import DB_SCHEMA, DB_PATH

def init_db():
    """
    Initializes the database schema using the constants defined in src/constants.py.

    This function ensures that the 'expenses' table exists and sets up necessary 
    foreign key constraints. It should be called once when the application starts.
    """
    try:
        from src.constants import DB_SCHEMA  # Required dependency for schema definition
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON;")
            cur.execute(DB_SCHEMA)
            conn.commit()
    except (sqlite3.Error, ImportError) as e:
        print(f"SQLite3 Error during initialization or missing constants: {e}")


def add_expense(expense: Expense, db_path: str = None):
    """
    Persists a new expense record into the database.

    Args:
        expense (Expense): The structured expense data to save.
        db_path (str, optional): The path to the SQLite database file. 
            If None, uses the default expenses.db location.

    Returns:
        int or None: The inserted ID if successful, None otherwise.
    """
    conn_path = db_path if db_path else DB_PATH
    try:
        with sqlite3.connect(conn_path) as conn:
            cur = conn.cursor()
            query = "INSERT INTO expenses(amount, category, description, date) VALUES(?,?,?,?)"
            params = (expense.amount, expense.category, expense.description, expense.date)
            cur.execute(query, params)
            conn.commit()
            return cur.lastrowid  # Return the newly created ID
    except sqlite3.Error as e:
        print(f"SQLite3 Error during insertion: {e}")
        return None


def get_expenses_by_id(expense_id, db_path: str = None):
    """
    Retrieve a single expense record by its ID.

    Args:
        expense_id (int): The unique identifier of the expense to retrieve.
        db_path (str, optional): The path to the SQLite database file. 
            If None, uses the default expenses.db location.

    Returns:
        Expense or None: The expense object with id set, or None if not found.
    """
    conn_path = db_path if db_path else DB_PATH
    try:
        with sqlite3.connect(conn_path) as conn:
            cursor = conn.cursor()
            query = "SELECT id, amount, category, description, date FROM expenses WHERE id=?"
            params = (expense_id,)
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row is None:
                return None
            # Correct instantiation order: (amount, category, description, date, id)
            exp = Expense(row[1], row[2], row[3], row[4], row[0])
            return exp
    except sqlite3.Error as e:
        print(f"ERROR reading expense: {e}")
        return None


def get_all_expenses(db_path: str = None):
    """
    Retrieve all expenses from the database.

    Args:
        db_path (str, optional): The path to the SQLite database file. 
            If None, uses the default expenses.db location.

    Returns:
        list[Expense]: A list of Expense objects with IDs set, ordered by ID (newest first).
    """
    conn_path = db_path if db_path else DB_PATH
    try:
        with sqlite3.connect(conn_path) as conn:
            cursor = conn.cursor()
            # Ordering by id DESC to show newest expenses first in the console/list view
            query = "SELECT id, amount, category, description, date FROM expenses ORDER BY id DESC"
            params = ()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            result = []
            for r in rows:
                # Correct instantiation order: (amount, category, description, date, id)
                exp = Expense(r[1], r[2], r[3], r[4], r[0])
                result.append(exp)
            return result
    except sqlite3.Error as e:
        print(f"ERROR reading expenses: {e}")
        return []


def update_expense(expense_id, amount, category, description, date, db_path: str = None):
    """
    Update an existing expense record.

    Args:
        expense_id (int): The unique identifier of the expense to update.
        amount (str): New amount value.
        category (str): New category.
        description (str): New description.
        date (str): New date in DD/MM/YYYY format.
        db_path (str, optional): The path to the SQLite database file. 
            If None, uses the default expenses.db location.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn_path = db_path if db_path else DB_PATH
    try:
        with sqlite3.connect(conn_path) as conn:
            cur = conn.cursor()
            query = "UPDATE expenses SET amount=?, category=?, description=?, date=? WHERE id=?"
            params = (amount, category, description, date, expense_id)
            cur.execute(query, params)
            if cur.rowcount == 0:
                print(f"WARNING: No record found with ID {expense_id}")
                return False
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"ERROR updating expense: {e}")
        return False


def delete_expense(expense_id, db_path: str = None):
    """
    Delete an expense record by its ID.

    Args:
        expense_id (int): The unique identifier of the expense to delete.
        db_path (str, optional): The path to the SQLite database file. 
            If None, uses the default expenses.db location.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    conn_path = db_path if db_path else DB_PATH
    try:
        with sqlite3.connect(conn_path) as conn:
            cur = conn.cursor()
            query = "DELETE FROM expenses WHERE id=?"
            params = (expense_id,)
            cur.execute(query, params)
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"SQLite3 Error during deletion: {e}")
        return False
