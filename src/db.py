"""
Data Access Object (DAO) for Expenses.

Handles all low-level database interactions using SQLite. It abstracts 
the complexity of connection management and transaction execution from the rest of the application.
All functions here cause side effects by writing to or reading from 'expenses.db'.
"""
import os
import sqlite3
from src.expense import Expense
from src.constants import DB_SCHEMA

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "..", "expenses.db")

def init_db():
    """
    Initializes the database schema.

    This function ensures that the 'expenses' table exists in the local 
    database file and sets up necessary foreign key constraints.
    It should be called exactly once when the application starts.

    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute(DB_SCHEMA)
        cur.close()
    except sqlite3.Error as e:
        print(f"SQLite3 Error: {e}")

def add_expense(expense: Expense, db_name):
    """
    Persists a new expense record into the database.

    Args:
        expense (Expense): The structured expense data to save.

    """
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("""INSERT INTO expenses(amount, category, description, date)
                    VALUES(?,?,?,?)
        """, (expense.amount, expense.category, expense.description, expense.date))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite3 Error: {e}")
