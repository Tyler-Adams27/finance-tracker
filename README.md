# Finance Tracker

A simple command-line application built in Python to help users track their personal finances by managing expenses. It persists all data locally using an SQLite database.

## Features

*   **Expense Tracking:** Easily record new expenses including amount, category, description, and date.
*   **Data Persistence:** All recorded transactions are saved safely in a local `expenses.db` SQLite database.
*   **CRUD Operations:** Provides full functionality to **List**, **Add**, **Edit**, and **Delete** expense records via the command line interface.

## Setup & Installation

The project is designed to run using Python. Please ensure you have Python installed on your system.

1.  **Install Dependencies:**
    Since this project uses specific libraries, first install the required dependencies listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    Execute the main entry point script:
    ```bash
    python src/console.py
    ```

## Usage Guide

Upon running the application, a menu will be displayed with the following options:

*   **1: Add a new expense.** Follow the prompts to enter the amount, category, description, and date for your transaction.
*   **2: Edit an expense.** Select an existing entry to modify its details.
*   **3: Delete an expense.** Remove a recorded transaction permanently.
*   **4: List all expenses.** View a summary of every expense currently stored in the tracker.

## Codebase Structure

The application follows a modular design pattern within the `src/` directory:

*   **`expense.py`:** Defines the core data structure (`Expense`) used throughout the application, ensuring consistency for amount, category, description, and date attributes.
*   **`db.py`:** Handles all database interactions using SQLite. It manages connecting to `expenses.db`, initializing the necessary tables, and executing CRUD queries (like `add_expense`).
*   **`console.py`:** Contains the main user interface logic (`console()` function), handling menu presentation and directing user input to the appropriate modules.
*   **`main.py`:** (Currently empty/placeholder) This file acts as the primary application entry point, although `src/console.py` is currently called directly in setup instructions.

***
Disclaimer: This documentation and any debugging assistance provided were generated with the help of an AI assistant. The core application logic and code in the repository are written manually by myself.
