# Imports the Flask framework to build the server, serve HTML pages, read incoming data, and send JSON responses
from flask import Flask, render_template, jsonify, request
# Imports the built-in operating system tool to manage files and folders (though not actively used below)
import os
# Imports the lightweight built-in database system to save and retrieve files permanently
import sqlite3

# Creates your main Flask web application instance and names it after this file context
app = Flask(__name__)
# Defines a global variable holding the exact file name where your budget data will be stored on your hard drive
DB_FILE = 'expenses.db'

# Starts a custom function block designed to set up your storage space when the app launches
def init_db():
    """Creates the SQLite database file and table if they do not exist."""
    # Establishes a secure connection line to your local database file, closing it automatically when finished
    with sqlite3.connect(DB_FILE) as conn:
        # Opens an active workspace pointer (cursor) inside the file to run structural data commands
        cursor = conn.cursor()
        # Executes an SQL command to safely construct an 'expenses' sheet layout only if it is missing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        ''')
        # Saves the structural table changes permanently down into the physical database file
        conn.commit()

# Tells the web server to listen for users navigating to the main, root homepage URL address (/)
@app.route('/')
# Starts the function block that runs whenever someone loads your core homepage address
def home():
    """Serves your index.html file to the browser."""
    # Instructs Flask to find your 'index.html' file inside your templates folder and display it on screen
    return render_template('index.html')

# Setup a data pathway specifically for fetching data ('GET') using the web path /api/expenses
@app.route('/api/expenses', methods=['GET'])
# Starts the function block meant to collect and deliver your complete history list
def get_expenses():
    """Retrieves all expenses from the database."""
    # Opens up a secure connection line to access your stored budget file records
    with sqlite3.connect(DB_FILE) as conn:
        # Opens an active workspace pointer (cursor) to look up your financial rows
        cursor = conn.cursor()
        # Executes an SQL query requesting the tracking ID, description, category, and price of all entries
        cursor.execute('SELECT id, description, category, amount FROM expenses')
        # Grabs every single row found by the database query and dumps them into a raw list variable
        rows = cursor.fetchall()
        
    # Loops through the raw data rows and rearranges them into neat Python dictionary labels for clarity
    expenses = [{'id': r[0], 'description': r[1], 'category': r[2], 'amount': r[3]} for r in rows]
    # Converts the labeled Python list into a web-readable JSON format and sends it back to the browser
    return jsonify(expenses)

# Setup a data pathway specifically for receiving and saving data ('POST') at /api/expenses
@app.route('/api/expenses', methods=['POST'])
# Starts the function block meant to process a newly submitted expense entry
def add_expense():
    """Saves a new expense sent from the frontend into the database."""
    # Catches the incoming raw data package sent across the web from your HTML submission form
    data = request.json
    # Extracts the specific item name typed into the 'description' field of the incoming package
    desc = data.get('description')
    # Extracts the specific category option selected in the 'category' field of the incoming package
    cat = data.get('category')
    # Extracts the specific numerical price cost typed into the 'amount' field of the incoming package
    amt = data.get('amount')

    # Opens up a secure connection line to write data into your database storage file
    with sqlite3.connect(DB_FILE) as conn:
        # Opens an active workspace pointer (cursor) to insert new information rows
        cursor = conn.cursor()
        # Securely injects the description, category, and amount into your expenses table using safe placeholders (?)
        cursor.execute(
            'INSERT INTO expenses (description, category, amount) VALUES (?, ?, ?)',
            (desc, cat, amt)
        )
        # Saves the newly added entry line permanently down into the physical file
        conn.commit()
    # Sends a success note back to the browser alongside code 201 meaning 'Item Created Successfully'
    return jsonify({'status': 'success'}), 201

# Setup a dynamic data pathway to delete an item based on its unique trailing ID number
@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
# Starts the function block that handles target removal, passing in the specific ID number to drop
def delete_expense(expense_id):
    """Removes a specific expense row from the database using its ID."""
    # Opens up a secure connection line to target changes inside your data records
    with sqlite3.connect(DB_FILE) as conn:
        # Opens an active workspace pointer (cursor) to modify target database entries
        cursor = conn.cursor()
        # Executes an SQL command searching for and erasing the one entry whose unique ID matches your request
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        # Saves the deletion change permanently down into the physical database file
        conn.commit()
    # Sends a clean JSON success confirmation message back to your frontend interface
    return jsonify({'status': 'success'})

# Setup a data pathway specifically for clearing out data ('POST') at the reset endpoint
@app.route('/api/expenses/reset', methods=['POST'])
# Starts the function block triggered by clicking your interface 'Reset Database' button
def reset_database():
    """Deletes all expense rows from the database table."""
    # Opens up a secure connection line to access your stored budget file records
    with sqlite3.connect(DB_FILE) as conn:
        # Opens an active workspace pointer (cursor) to sweep your storage data sheets
        cursor = conn.cursor()
        # Executes a wiping command that completely empties out every single entry row inside your tracker table
        cursor.execute('DELETE FROM expenses')
        # Saves the complete table wipe change permanently down into the physical file
        conn.commit()
    # Sends a clear JSON success note confirming the database is wiped clean back to your browser
    return jsonify({'status': 'success', 'message': 'Database cleared'})

# A safety check ensuring this script only boots up the web server if run directly (not loaded by another file)
if __name__ == '__main__':
    # Initialises the database layout rows by executing the custom setup function defined at the top
    init_db()
    # Activates the live local Flask server with active debug tools on, meaning it auto-updates when you edit code
    app.run(debug=True)
