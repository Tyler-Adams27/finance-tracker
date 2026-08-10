"""
 The console
"""
from expense import Expense
from db import add_expense
def console():
    """
    The console implementation
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
    Add a new expense.
    """
    while True:
        new_amount = input("Amount: ").strip()
        new_category = input("Category: ").strip()
        new_description = input("Description: ").strip()
        new_date = input("Date: ").strip()

        # Check if the fields are empty
        if not new_amount or not new_category or not new_description or not new_date:
            print("Fields cannot be empty!")
            continue
        new_expense_obj = Expense(new_amount, new_category, new_description, new_date)
        try:
            add_expense(new_expense_obj)
            print("Expense added successfully!")
            break
        except ValueError as e:
            print(f"Error: {e}")

def edit_expense():
    """
    Edit an expense.
    """
def delete_expense():
    """
    Delete a expense.
    """
def list_expenses():
    """
    List all expenses.
    """

console()
