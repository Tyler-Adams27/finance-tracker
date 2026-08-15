def new_expense():
    """
    Guides the user through adding a brand-new expense record via CLI prompts.

    Interacts with the database layer to persist the structured data upon successful input.
    Side Effect: Calls add_expense() to modify expenses.db.
    """
    while True:
        try:
            new_amount = input("Amount: ").strip()
            validate_amount(new_amount)
        except ValueError:
            print("Amount must be numeric (e.g 10 or 10.99)")
            return False

        new_category = input("Category: ").strip()
        validate_category(new_category)

        new_description = input("Description: ").strip()
        new_date = input("Date: ").strip()

        # Input validation
            # - Amount must be in "??.??" format.
            # - Category must not contain symbols.
            # - Description can be anything.
            # - Date must follow "DD/MM/YYYY" format.
            # Check if the fields are empty.
        if not new_amount or not new_category or not new_description or not new_date:
            print("Fields cannot be empty!")

        try:
            datetime.strptime(new_date, "%d/%m/%Y")

        except ValueError:
            print("Incorrect date format. Use DD/MM/YYYY")
            continue

        new_expense_obj = Expense(new_amount, new_category, new_description, new_date)

        try:
            add_expense(new_expense_obj, DB_PATH)
            print("Expense added successfully!")
            break

        except ValueError as e:
            print(f"Error: {e}")