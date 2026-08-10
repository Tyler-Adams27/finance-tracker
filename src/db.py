"""
The database implementation.
"""
import sqlite3
from expense import Expense

def init_db():
    """
    Connect to db
    """
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        amount TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        date TEXT NOT NULL
    );

""")

def add_expense(expense: Expense):
    """
    Add an expense
    """
    conn = sqlite3.connect("../expenses.db")
    cur = conn.cursor()
    cur.execute("""INSERT INTO expenses(amount, category, description, date)
                VALUES(?,?,?,?)
    """, (expense.amount, expense.category, expense.description, expense.date))
    conn.commit()
