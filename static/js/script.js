const API_BASE = 'http://localhost:5000/api';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('entry-date').value = today;
    document.getElementById('tb-date').value = today;
    document.getElementById('pl-end-date').value = today;

    // Load initial data
    loadAccounts();
    loadJournalEntries();

    // Setup tab navigation
    setupTabs();

    // Setup forms
    setupForms();
});

function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked
            btn.classList.add('active');
            document.getElementById(tabName).classList.add('active');

            // Reload data when switching tabs
            if (tabName === 'accounts') loadAccounts();
            if (tabName === 'daybook') loadJournalEntries();
        });
    });
}

function setupForms() {
    // Account form
    document.getElementById('account-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            account_code: document.getElementById('account-code').value,
            account_name: document.getElementById('account-name').value,
            account_type: document.getElementById('account-type').value
        };

        try {
            const response = await fetch(`${API_BASE}/accounts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                alert('Account added successfully!');
                e.target.reset();
                loadAccounts();
            } else {
                alert('Error adding account');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });

    // Journal form
    document.getElementById('journal-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            date: document.getElementById('entry-date').value,
            account_code: document.getElementById('entry-account').value,
            particulars: document.getElementById('entry-particulars').value,
            debit: parseFloat(document.getElementById('entry-debit').value) || 0,
            credit: parseFloat(document.getElementById('entry-credit').value) || 0
        };

        // Validation
        if (data.debit === 0 && data.credit === 0) {
            alert('Either debit or credit must be non-zero');
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/journal`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                alert('Journal entry added successfully!');
                e.target.reset();
                document.getElementById('entry-date').value = new Date().toISOString().split('T')[0];
                document.getElementById('entry-debit').value = 0;
                document.getElementById('entry-credit').value = 0;
                loadJournalEntries();
            } else {
                alert('Error adding journal entry');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });

    // Import form
    document.getElementById('import-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('excel-file');
        const file = fileInput.files[0];

        if (!file) {
            alert('Please select a file');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE}/import-excel`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            const resultDiv = document.getElementById('import-result');

            if (response.ok) {
                resultDiv.innerHTML = `<div class="success">Successfully imported ${result.imported_count} entries!</div>`;
                fileInput.value = '';
                setTimeout(() => resultDiv.innerHTML = '', 5000);
            } else {
                resultDiv.innerHTML = `<div class="error">Error: ${result.error}</div>`;
            }
        } catch (error) {
            document.getElementById('import-result').innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    });
}

async function loadAccounts() {
    try {
        const response = await fetch(`${API_BASE}/accounts`);
        const accounts = await response.json();

        const tbody = document.getElementById('accounts-tbody');
        tbody.innerHTML = '';

        accounts.forEach(account => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${account.account_code}</td>
                <td>${account.account_name}</td>
                <td>${account.account_type}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteAccount('${account.account_code}')">Delete</button>
                </td>
            `;
        });
    } catch (error) {
        console.error('Error loading accounts:', error);
    }
}

async function deleteAccount(accountCode) {
    if (!confirm('Are you sure you want to delete this account?')) return;

    try {
        const response = await fetch(`${API_BASE}/accounts/${accountCode}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Account deleted successfully!');
            loadAccounts();
        } else {
            alert('Error deleting account');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function loadJournalEntries() {
    const startDate = document.getElementById('filter-start-date').value;
    const endDate = document.getElementById('filter-end-date').value;

    let url = `${API_BASE}/journal?`;
    if (startDate) url += `start_date=${startDate}&`;
    if (endDate) url += `end_date=${endDate}&`;

    try {
        const response = await fetch(url);
        const entries = await response.json();

        const tbody = document.getElementById('journal-tbody');
        tbody.innerHTML = '';

        entries.forEach(entry => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${entry.date}</td>
                <td>${entry.account_code}</td>
                <td>${entry.particulars}</td>
                <td class="text-right">${formatCurrency(entry.debit)}</td>
                <td class="text-right">${formatCurrency(entry.credit)}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteJournalEntry(${entry.id})">Delete</button>
                </td>
            `;
        });
    } catch (error) {
        console.error('Error loading journal entries:', error);
    }
}

async function deleteJournalEntry(entryId) {
    if (!confirm('Are you sure you want to delete this entry?')) return;

    try {
        const response = await fetch(`${API_BASE}/journal/${entryId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Entry deleted successfully!');
            loadJournalEntries();
        } else {
            alert('Error deleting entry');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function loadLedger() {
    const accountCode = document.getElementById('ledger-account').value;
    if (!accountCode) {
        alert('Please enter an account code');
        return;
    }

    const startDate = document.getElementById('ledger-start-date').value;
    const endDate = document.getElementById('ledger-end-date').value;

    let url = `${API_BASE}/ledger/${accountCode}?`;
    if (startDate) url += `start_date=${startDate}&`;
    if (endDate) url += `end_date=${endDate}&`;

    try {
        const response = await fetch(url);
        const entries = await response.json();

        const tbody = document.getElementById('ledger-tbody');
        tbody.innerHTML = '';

        if (entries.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No entries found</td></tr>';
            return;
        }

        entries.forEach(entry => {
            const row = tbody.insertRow();
            const balanceClass = entry.balance >= 0 ? '' : 'text-danger';
            row.innerHTML = `
                <td>${entry.date}</td>
                <td>${entry.particulars}</td>
                <td class="text-right">${formatCurrency(entry.debit)}</td>
                <td class="text-right">${formatCurrency(entry.credit)}</td>
                <td class="text-right ${balanceClass}">${formatCurrency(Math.abs(entry.balance))}</td>
            `;
        });
    } catch (error) {
        console.error('Error loading ledger:', error);
        alert('Error loading ledger');
    }
}

async function loadTrialBalance() {
    const endDate = document.getElementById('tb-date').value;

    try {
        const response = await fetch(`${API_BASE}/trial-balance?end_date=${endDate}`);
        const data = await response.json();

        const tbody = document.getElementById('trial-balance-tbody');
        const tfoot = document.getElementById('trial-balance-tfoot');
        tbody.innerHTML = '';

        data.accounts.forEach(account => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${account.account_code}</td>
                <td>${account.account_name}</td>
                <td class="text-right">${formatCurrency(account.debit_balance)}</td>
                <td class="text-right">${formatCurrency(account.credit_balance)}</td>
            `;
        });

        tfoot.innerHTML = `
            <tr>
                <td colspan="2"><strong>Total</strong></td>
                <td class="text-right"><strong>${formatCurrency(data.total_debit)}</strong></td>
                <td class="text-right"><strong>${formatCurrency(data.total_credit)}</strong></td>
            </tr>
        `;
    } catch (error) {
        console.error('Error loading trial balance:', error);
        alert('Error loading trial balance');
    }
}

async function loadProfitLoss() {
    const startDate = document.getElementById('pl-start-date').value;
    const endDate = document.getElementById('pl-end-date').value;

    let url = `${API_BASE}/profit-loss?`;
    if (startDate) url += `start_date=${startDate}&`;
    if (endDate) url += `end_date=${endDate}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        // Expenses
        const expensesTbody = document.getElementById('expenses-tbody');
        const expensesTfoot = document.getElementById('expenses-tfoot');
        expensesTbody.innerHTML = '';

        data.expenses.forEach(expense => {
            const row = expensesTbody.insertRow();
            row.innerHTML = `
                <td>${expense.account_name}</td>
                <td class="text-right">${formatCurrency(expense.amount)}</td>
            `;
        });

        expensesTfoot.innerHTML = `
            <tr>
                <td><strong>Total Expenses</strong></td>
                <td class="text-right"><strong>${formatCurrency(data.total_expenses)}</strong></td>
            </tr>
        `;

        // Income
        const incomeTbody = document.getElementById('income-tbody');
        const incomeTfoot = document.getElementById('income-tfoot');
        incomeTbody.innerHTML = '';

        data.income.forEach(income => {
            const row = incomeTbody.insertRow();
            row.innerHTML = `
                <td>${income.account_name}</td>
                <td class="text-right">${formatCurrency(income.amount)}</td>
            `;
        });

        incomeTfoot.innerHTML = `
            <tr>
                <td><strong>Total Income</strong></td>
                <td class="text-right"><strong>${formatCurrency(data.total_income)}</strong></td>
            </tr>
        `;

        // Net Profit
        const netProfitDisplay = document.getElementById('net-profit-display');
        const profitClass = data.net_profit >= 0 ? '' : 'text-danger';
        const profitLabel = data.net_profit >= 0 ? 'Net Profit' : 'Net Loss';
        netProfitDisplay.innerHTML = `${profitLabel}: ₹${formatCurrency(Math.abs(data.net_profit))}`;
    } catch (error) {
        console.error('Error loading profit & loss:', error);
        alert('Error loading profit & loss statement');
    }
}

function formatCurrency(amount) {
    if (amount === 0 || amount === null || amount === undefined) return '0.00';
    return parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}
