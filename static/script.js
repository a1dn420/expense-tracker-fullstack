// Finds the HTML text entry box for the item name and stores it in a JavaScript variable
const descriptionInput = document.getElementById('description');
// Finds the HTML number input box for the item price and stores it in a JavaScript variable
const amountInput = document.getElementById('amount');
// Finds the HTML dropdown menu box for the item category and stores it in a JavaScript variable
const categoryInput = document.getElementById('category');
// Finds the HTML 'Add Expense' button and stores it in a JavaScript variable
const addBtn = document.getElementById('add-btn');
// Finds the empty HTML table body where the rows will go and stores it in a JavaScript variable
const expenseList = document.getElementById('expense-list');
// Finds the HTML span tags isolating the '0.00' total price number and stores it in a JavaScript variable
const totalAmountSpan = document.getElementById('total-amount');

// Creates an asynchronous function to load saved items from the server without freezing the screen
async function loadExpenses() {
    // Sends a web request to your Python server to fetch the raw database entries and waits for them
    const response = await fetch('/api/expenses');
    // Translates the server's raw web response package into a readable JavaScript list format
    const expenses = await response.json();
    
    // Wipes out any old HTML rows sitting inside your table body to prepare for a clean redraw
    expenseList.innerHTML = '';
    // Sets up a temporary digital tally counter starting at zero to recalculate your total spending
    let total = 0;

    // Loops through every individual expense item found inside the database list one by one
    expenses.forEach(expense => {
        // Adds the current loop item's price directly onto your running total counter tally
        total += expense.amount;

        // Creates a brand new, empty HTML table row element (<tr>) inside the computer's memory
        const row = document.createElement('tr');
        // Fills the fresh row with HTML data columns containing the matching item properties
        row.innerHTML = `
            <td>${expense.description}</td>
            <td>${expense.category}</td>
            <td>£${expense.amount.toFixed(2)}</td>
            <td><button class="delete-btn" onclick="deleteExpense(${expense.id})">Delete</button></td>
        `;
        // Shoves the newly built data row directly into your visible HTML web page table body
        expenseList.appendChild(row);
    });

    // Rewrites the total text on your screen, forcing it to always show exactly 2 decimal places (like £0.00)
    totalAmountSpan.innerText = total.toFixed(2);
}

// Creates an asynchronous function to process and send a brand new input form entry to the server
async function addExpense() {
    // Grabs the text typed in the description box and trims off any accidental blank spaces from the edges
    const desc = descriptionInput.value.trim();
    // Grabs the text inside the amount box and converts it from standard text into a true decimal number
    const amt = parseFloat(amountInput.value);
    // Grabs whichever category string value is currently selected inside the dropdown menu element
    const cat = categoryInput.value;

    // Checks if description is empty, or if the number is broken, or if the user entered zero/negative cash
    if (desc === '' || isNaN(amt) || amt <= 0) {
        // Pops up a warning alert message dialog box on the screen telling the user they made a mistake
        alert('Please enter a valid description and amount!');
        // Halts the function immediately so bad or empty data never touches your database
        return;
    }

    // Sends an asynchronous web post request pushing the new data object straight down into your Python API
    await fetch('/api/expenses', {
        // Tells the server that you are submitting new data instead of just looking up records
        method: 'POST',
        // Attaches digital headers telling the server to read this package as standard JSON format
        headers: { 'Content-Type': 'application/json' },
        // Flattens your structured JavaScript dictionary properties into a single text string line for transport
        body: JSON.stringify({ description: desc, category: cat, amount: amt })
    });

    // Clears the item text input box back to a blank state so it is ready for your next entry
    descriptionInput.value = '';
    // Clears the price input box back to a blank state so it is ready for your next entry
    amountInput.value = '';
    
    // Automatically runs your loading function to grab the updated table rows and refresh the display
    loadExpenses();
}

// Registers a destruction function globally on the browser window so the HTML delete buttons can find it
window.deleteExpense = async function(id) {
    // Contacts the specific Python delete server route, appending the unique item ID number onto the URL path
    await fetch(`/api/expenses/${id}`, { method: 'DELETE' });
    // Refreshes the display list to instantly remove the deleted row from the user's screen view
    loadExpenses();
};

// Listens for a mouse click on the 'Add Expense' button and runs your custom processing function when fired
addBtn.addEventListener('click', addExpense);

// Runs the lookup function once immediately right when the page finishes booting up in the browser
loadExpenses();

// Finds the HTML 'Reset Database' button element and assigns it to a clean JavaScript variable
const resetBtn = document.getElementById('reset-btn');

// Creates an asynchronous function to clear out your complete history archive loop across the backend
async function resetDatabase() {
    // Shows a pop-up confirmation warning box asking the user to click OK or Cancel before deleting
    const confirmClear = confirm("Are you sure you want to completely clear your expense logs?");
    
    // If the user clicks the OK button inside the confirmation window, run this internal action block
    if (confirmClear) {
        // Sends an asynchronous request triggering the backend database wiping sequence route
        await fetch('/api/expenses/reset', { method: 'POST' });
        // Refreshes your visual interface layout grids to confirm everything has been completely cleared out
        loadExpenses();
    }
}

// Listens for a mouse click on the 'Reset Database' button and kicks off your confirmation logic
resetBtn.addEventListener('click', resetDatabase);
