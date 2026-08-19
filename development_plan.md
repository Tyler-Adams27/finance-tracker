# Development Plan: From CLI Tool to Web Application

This document outlines the phased approach for evolving the Finance Tracker from its current Command Line Interface (CLI) tool into a fully functional web application using Flask.

## Stage 1: Core Structure & Command Line Interface (Current State)

**Goal:** Establish and stabilize the foundational logic, data handling, and user interaction flow entirely through the command line.

**Status:** **In Progress.**
The project currently adheres to this stage. The core functionalities are in place:
*   **Data Model (`src/expense.py`):** Defines the `Expense` structure.
*   **Database Layer (`src/db.py`):** Manages SQLite persistence, ensuring reliable CRUD operations against `expenses.db`.
*   **Interface (`src/console.py`):** Provides the complete CLI user experience for adding, listing, editing, and deleting expenses.

**Key Achievements:**
*   Data integrity is maintained through defined classes and database transactions.
*   The application is stable for local testing and usage via `python src/console.py`.

## Stage 2: Web Application Implementation (Flask Server)

**Goal:** Migrate the existing core logic to a web framework, providing an accessible Graphical User Interface (GUI) via a Flask server.

**Tasks & Milestones:**
1.  **Backend Refactoring:** The `src/db.py` and `src/expense.py` modules will be kept largely intact but adapted to be accessed by a RESTful API structure rather than direct script calls.
2.  **Flask Setup:** Initialize the Flask server in the main entry point (e.g., renaming or modifying `main.py`). This involves setting up routing for different functionalities (e.g., `/add`, `/list`, `/edit/<id>`).
3.  **API Endpoints:** Create backend routes that mirror CLI actions:
    *   `POST /expenses/`: Handles adding a new expense (receives JSON data).
    *   `GET /expenses`: Retrieves all expenses (or filtered lists).
    *   `PUT /expenses/<id>`: Updates an existing expense.
    *   `DELETE /expenses/<id>`: Deletes an expense record.
4.  **Frontend Development:** Build the web forms and presentation layer using HTML/CSS/Jinja2 templates that interact with the new Flask API endpoints. This will replace the `print()` and `input()` calls currently in `src/console.py`.

**Expected Outcome:**
A fully functional web portal where users can manage their expenses through a graphical interface, while leveraging the robust data handling layer built during Stage 1.