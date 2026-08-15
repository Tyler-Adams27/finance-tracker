"""
 The console
"""
import os
from src.expense import Expense
from src.db import add_expense
from src.validators import validate_amount, validate_category, validate_description, validate_date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "..", "expenses.db")

def console():
    """
    Runs the main command-line loop for the Finance Tracker CLI.

    This function presents the primary menu to the user and calls 
    the appropriate handler based on input (Add, Edit, Delete, List).
    It manages the overall state of the CLI session until manually exited.
    """


    user_input = ""
    exit_program = False

    while not exit_program:

        print("-------------------")
        print("THE FINANCE TRACKER")
        print("-------------------\n")
        print("Here are your options:\n")
        print("1: Add a new expense.")
        print("2: Edit an expense.")
        print("3: Delete an expense.")
        print("4: List all expenses.")
        print("Q: Close program.\n")

        user_input = input("")

        match user_input:
            case "1":
                new_expense()
            case "2":
                edit_expense()
            case "3":
                delete_expense()
            case "4":
                list_expenses()
            case "Q":
                exit_program = True
            case _:
                pass

def new_expense():
    """
    Create a new expense, and enter it into the database.
    """
    while True:
        new_amount = input("Amount: ").strip()
        if not validate_amount(new_amount):
            print("Amount must be numeric (e.g 10 or 10.99)")
            continue
        else:
            break

    while True:
        new_category = input("Category: ").strip()
        if not validate_category(new_category):
            print("Category can only contain alphabetic characters and spaces")
            continue
        else:
            break

    while True:
        new_description = input("Description: ").strip()
        if not validate_description(new_description):
            print("Description must not be empty")
            continue
        else:
            break

    while True:
        new_date = input("Date: ").strip()
        if not validate_date(new_date):
            print("Date is in the wrong format (Use DD/MM/YYYY)")
            continue
        else:
            break
    try:
        created_expense = Expense(new_amount, new_category, new_description, new_date)
        add_expense(created_expense, "expenses.db")
    except ValueError as e:
        print(f"ERROR: {e}")

def edit_expense():
    """
    Handles the logic flow for modifying an existing expense record.

    In a future web implementation (Stage 2), this function will be replaced by
    an API endpoint handler that processes IDs and JSON payloads.
    """
def delete_expense():

    """
    Manages the logic flow for removing a recorded expense record.

    This function prompts the user to specify which expense by ID or criteria 
    should be permanently removed from the system.
    """
def list_expenses():
    """
    Retrieves and displays all stored expenses to the user.

    This function calls the database layer to fetch records and then 
    formats and prints them in a readable format to the console.
    Side Effect: Reads from expenses.db and prints output to the console.
    """
