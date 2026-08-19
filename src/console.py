"""
The console
"""
import os
import sqlite3
from src.expense import Expense
from src.db import add_expense, get_all_expenses, update_expense, delete_expense, init_db
from src.constants import DB_SCHEMA, DB_PATH
from src.validators import validate_amount, validate_category, validate_description, validate_date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def console():
    """
    Runs the main command-line loop for the Finance Tracker CLI.

    This function presents the primary menu to the user and calls 
    the appropriate handler based on input (Add, Edit, Delete, List).
    It manages the overall state of the CLI session until manually exited.
    """
    user_input = ""
    exit_program = False

    # Initialize database connection immediately upon running the console
    init_db() 

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
                handle_delete_expense() # Use the consistently named function
            case "4":
                list_expenses()
            case "Q":
                exit_program = True
            case _:
                print("Invalid option. Please choose 1-4 or Q to quit.\n")


def new_expense():
    """
    Create a new expense, and enter it into the database.
    """
    while True:
        new_amount = input("Amount: ").strip()
        if not validate_amount(new_amount):
            print("Amount must be numeric (e.g 10 or 10.99)")
            continue
        break

    while True:
        new_category = input("Category: ").strip()
        if not validate_category(new_category):
            print("Category can only contain alphabetic characters and spaces")
            continue
        break

    while True:
        new_description = input("Description: ").strip()
        if not validate_description(new_description):
            print("Description must not be empty")
            continue
        break

    while True:
        new_date = input("Date: ").strip()
        if not validate_date(new_date):
            print("Date is in the wrong format (Use DD/MM/YYYY)")
            continue
        break
    try:
        created_expense = Expense(new_amount, new_category, new_description, new_date)
        # Use DB_PATH for consistency
        add_expense(created_expense, DB_PATH)
        print("Expense added successfully!\n")
    except ValueError as e:
        print(f"ERROR: {e}")


def edit_expense():
    """
    Handles the logic flow for modifying an existing expense record.

    In a future web implementation (Stage 2), this function will be replaced by
    an API endpoint handler that processes IDs and JSON payloads.
    """
    print("\n--- Edit Expense ---")

    # First, display all expenses so user can select one to edit
    expenses = get_all_expenses()
    if not expenses:
        print("No expenses recorded yet. Use option 1 to add one.")
        return

    print("\nCurrent Expenses:")
    for i, exp in enumerate(expenses, 1):
        print(f"  {i}. ${exp.amount} - {exp.category} - {exp.description} ({exp.date})")

    while True:
        try:
            choice = input("\nEnter expense number to edit (or 'q' to cancel): ").strip()
            if choice.lower() == "q":
                return
            choice_int = int(choice)
            if 1 <= choice_int <= len(expenses):
                break
            print(f"Please enter a valid number between 1 and {len(expenses)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    selected_expense = expenses[choice_int - 1]

    # Get new values with validation, allowing user to keep existing values
    while True:
        tmp_amt = selected_expense.amount
        new_amount = input(f"Amount (current: {tmp_amt}, or press Enter to skip): ").strip()
        if not new_amount:
            break
        if not validate_amount(new_amount):
            print("Amount must be numeric (e.g 10 or 10.99)")
            continue
        break

    while True:
        tmp_cat = selected_expense.category
        new_category = input(f"Category (current: {tmp_cat}, or press Enter to skip): ").strip()
        if not new_category:
            break
        if not validate_category(new_category):
            print("Category can only contain alphabetic characters and spaces")
            continue
        break

    while True:
        tmp_desc = selected_expense.description
        new_description = input(f"Description (current: {tmp_desc}, or press Enter to skip): ").strip()
        if not new_description:
            break
        if not validate_description(new_description):
            print("Description must not be empty")
            continue
        break

    while True:
        tmp_date = selected_expense.date
        new_date = input(f"Date (current: {tmp_date}, or press Enter to skip): ").strip()
        if not new_date:
            break
        if not validate_date(new_date):
            print("Date is in the wrong format (Use DD/MM/YYYY)")
            continue
        break

    # Prepare update data - only include fields that were changed
    updated_data = {}
    # Correct logic for determining if a field was provided OR if it's mandatory
    amount_to_use = new_amount if new_amount else selected_expense.amount
    category_to_use = new_category if new_category else selected_expense.category
    description_to_use = new_description if new_description else selected_expense.description
    date_to_use = new_date if new_date else selected_expense.date

    # Perform the update
    try:
        result = update_expense(
            expense_id=selected_expense.id,
            amount=amount_to_use,
            category=category_to_use,
            description=description_to_use,
            date=date_to_use
        )
        if result:
            print("Expense updated successfully!\n")
    except ValueError as e:
        print(f"ERROR updating expense: {e}")


def handle_delete_expense():
    """
    Manages the logic flow for removing a recorded expense record.

    This function prompts the user to specify which expense by ID or criteria
    should be permanently removed from the system.
    """
    print("\n--- Delete Expense ---")

    # Display all expenses with IDs
    expenses = get_all_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\nCurrent Expenses:")
    for i, exp in enumerate(expenses, 1):
        # Use f-string formatting for consistency and readability
        print(f"  {i}. ${exp.amount} - {exp.category:<15} {exp.date:<12} {exp.description}")

    while True:
        try:
            choice = input("\nEnter expense number to delete (or 'q' to cancel): ").strip()
            if choice.lower() == "q":
                return
            choice_int = int(choice)
            if 1 <= choice_int <= len(expenses):
                break
            print(f"Please enter a valid number between 1 and {len(expenses)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    selected_expense = expenses[choice_int - 1]

    # Confirmation step for destructive action
    confirm_msg = f"\nAre you sure you want to delete expense #{selected_expense.id} "
    confirm_msg += f"($ {selected_expense.amount}, {selected_expense.category})? (y/n): "
    confirm = input(confirm_msg).strip().lower()

    if confirm == 'y':
        try:
            # Use the existing function name delete_expense for deletion logic call
            result = delete_expense(selected_expense.id) 
            if result:
                print("Expense deleted successfully!\n")
        except ValueError as e:
            print(f"ERROR deleting expense: {e}")
    else:
        print("Deletion cancelled.\n")


def list_expenses():
    """
    Retrieves and displays all stored expenses to the user.

    This function calls the database layer to fetch records and then 
    formats and prints them in a readable format to the console.
    Side Effect: Reads from expenses.db and prints output to the console.
    """
    print("\n--- All Expenses ---")

    expenses = get_all_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    # Print table header with aligned columns (ID, Amount, Category, Date, Description)
    print(f"{'ID':<5} {'Amount':>10} {'Category':<15} {'Date':<12} Description")
    print("-" * 60)

    for exp in expenses:
        # expense attributes: amount, category, description, date
        print(f"{exp.id:<5} ${exp.amount:>9}, {exp.category:<15} {exp.date:<12} {exp.description}")

    print(f"\nTotal: {len(expenses)} expense(s)\n")


# Database initialization happens inside console() function