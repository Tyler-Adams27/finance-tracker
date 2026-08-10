"""
This is the expense module.
"""
class Expense:
    """
    This is the expense class.
    """
    def __init__(self, amount: float, category: str, description: str, date: str):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date
