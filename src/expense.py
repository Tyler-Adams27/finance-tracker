"""
Data container module for Expense objects.

Defines the core data structure representing a single financial expense.
This module is primarily a data model layer and contains no business logic.
"""
from dataclasses import dataclass

@dataclass
class Expense:
    """
    Initializes an Expense instance.

    Args:
        amount (str): The monetary value of the expense.
        category (str): The spending category (e.g., 'Food', 'Rent').
        description (str): A detailed description of the purchase or expense.
        date (str): The date of the transaction in YYYY-MM-DD format.
    """
    amount: str
    category: str
    description: str
    date: str
