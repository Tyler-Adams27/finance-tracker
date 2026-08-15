"""
Checks if inputs are valid.
"""
import re
import datetime
def validate_amount(amount):
    """
    Validate the amount only contains numbers and periods.
    """
    try:
        amount_pattern = r"^\d+(\.\d{1,2})?$"
        if not re.match(amount_pattern, amount):
            raise ValueError
        if float(amount) <= 0:
            raise ValueError
        if not amount:
            raise ValueError
    except ValueError:
        return False
    return True

def validate_category(category):
    """
    Validate the category only contains alphabetic characters and spaces.
    """
    try:
        category_pattern = r"^[A-Za-z\s]+$"
        if not re.match(category_pattern, category):
            raise ValueError("Category can only contain alphabetic characters and spaces")
        if not category:
            raise ValueError
    except ValueError:
        return False
    return True

def validate_description(description):
    """
    Validate that the description is not empty.
    """
    try:
        if not description:
            raise ValueError
    except ValueError:
        return False
    return True

def validate_date(date):
    """
    Validate the structure of a date.
    """
    try:
        if not date:
            raise ValueError
        datetime.datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        return False
    return True
