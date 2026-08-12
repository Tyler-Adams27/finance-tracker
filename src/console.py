"""
 The console
"""
import os
import re
from datetime import datetime
from src.expense import Expense
from src.db import add_expense

# Ensures absolute path is correct
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "..", "expenses.db")

def console():
    """
    Runs the main command-line loop for the Finance Tracker CLI.

    This function presents the primary menu to the user and calls 
    the appropriate handler based on input (Add, Edit, Delete, List).
    It manages the overall state of the CLI session until manually exited.
    """
    exit_console = False
    user_input = ""

    while not exit_console:
        print("-------------------")
        print("THE FINANCE TRACKER")
        print("-------------------\n")
        print("Here are your options:\n")
        print("1: Add a new expense.")
        print("2: Edit an expense.")
        print("3: Delete an expense.")
        print("4: List all expenses.\n")

        user_input = input("")

        match user_input:
            case "1":
                exit_console = True
                new_expense()
            case "2":
                exit_console = True
                edit_expense()
            case "3":
                exit_console = True
                delete_expense()
            case "4":
                exit_console = True
                list_expenses()
            case _:
                pass

def new_expense():
    """
    Guides the user through adding a brand-new expense record via CLI prompts.

    Interacts with the database layer to persist the structured data upon successful input.
    Side Effect: Calls add_expense() to modify expenses.db.
    """
    while True:
        new_amount = input("Amount: ").strip()
        new_category = input("Category: ").strip()
        new_description = input("Description: ").strip()
        new_date = input("Date: ").strip()

        # Input validation
            # - Amount must be in "??.??" format.
            # - Category must not contain symbols (isAlpha()).
            # - Description can be anything.
            # - Date must follow "DD/MM/YYYY" format.
            # Check if the fields are empty.
        if not new_amount or not new_category or not new_description or not new_date:
            print("Fields cannot be empty!")
            continue

        if not new_category.isalpha():
            print("Category can only contain the alphabet!")
            continue

        try:
            datetime.strptime(new_date, "%d/%m/%Y")

        except ValueError:

            print("Incorrect date format. Use DD/MM/YYYY")
            continue

        amount_pattern = r"\d{2}\.\d{2}$"

        if not re.match(amount_pattern, new_amount):
            print("Amount is in the incorrect format. Use 00.00")
            continue



        new_expense_obj = Expense(new_amount, new_category, new_description, new_date)

        try:
            add_expense(new_expense_obj, DB_PATH)
            print("Expense added successfully!")
            break

        except ValueError as e:
            print(f"Error: {e}")

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

console()
