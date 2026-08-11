# Full-Stack Expense Tracker: System Integration & Debugging Case Study

## Project Overview
This project was built as an educational milestone to understand how frontend user interfaces communicate across system boundaries with backend server instances and persistent databases. 

Instead of focusing purely on syntax writing from scratch, this application served as a practical exercise in reverse-engineering, system architecture configuration, file routing, environment management, and browser-based network debugging.

---

## 🛠️ The Tech Stack
* **Frontend UI:** HTML5 for layout layout and Vanilla JavaScript (ES6) for network fetch requests.
* **Styling Framework:** Custom CSS3 utilizing CSS Flexbox for adaptive component formatting.
* **Backend Engine:** Python 3 utilizing the lightweight Flask Web Framework.
* **Database Engine:** Embedded SQLite3 for local, lightweight SQL data storage.

---

## 🔄 System Architecture & Data Flow
The application utilizes a classic three-tier architecture. Below is a breakdown of how data changes hands when an expense entry is processed:

1. **User Action:** The user inputs financial metrics into the HTML form fields and triggers the "Add Expense" button action.
2. **Network Transmission:** Custom JavaScript event listeners intercept the submit event, bundle the raw input metrics into a secure JSON package, and dispatch an asynchronous `HTTP POST` request via the browser `Fetch API` to the backend.
3. **Backend Processing:** The Python Flask application captures the payload on the `/api/expenses` endpoint routing layer, parses the values safely, opens a transactional context window with the SQLite database, and executes an `INSERT INTO` query.
4. **UI Update:** Upon a successful database response, the JavaScript application triggers an immediate `HTTP GET` request, receives the full list of database rows, recalculates the financial totals, and dynamically drops fresh rows straight into the DOM table layout without requiring a full browser page refresh.

---

## 🧠 Core Engineering Principles Learned

### 1. Environment Configurations & Path Failures
During initial project bootstrapping, the native system path failed to expose the standard `pip` and `python` executables via the terminal shell environment. I successfully troubleshot this environment blockage by identifying alternative Python wrapper shortcuts (`py app.py`) to properly execute background runtime server compilation tasks.

### 2. Strict Directory Routing (The Flask Paradigm)
Initially, the frontend web page loaded with missing style designs and broken button mechanics, displaying critical `404 Not Found` resource errors in the browser console. I resolved this issue by refactoring the local file hierarchy to strictly align with Flask's architecture requirements—segregating core layouts inside a dedicated `/templates` directory while hosting static network elements inside an accessible `/static` assets folder.

### 3. Asynchronous Data Management
Learned how to safely handle JavaScript Promises and `async/await` processing flows to prevent front-end race conditions, ensuring that table interfaces only attempt to update data displays *after* the local SQLite database file successfully writes data to disk.

---

## 🚀 How to Run Locally

1. Clone or download this project directory to your local file path.
2. Open your computer terminal inside the repository root directory.
3. Install the required web framework environment dependencies:
   ```bash
   py -m pip install Flask
   ```
4. Boot up the local runtime backend controller engine:
   ```bash
   py app.py
   ```
5. Open any web browser and navigate directly to your local loopback address:
   ```text
   http://127.0.0.1:5000
   ```
