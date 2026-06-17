# Accounting Management System

A comprehensive web-based accounting application for managing Daybook, Ledger, Trial Balance, and Profit & Loss accounts.

## Features

### 1. Daybook (Journal Entries)
- Add, view, and delete journal entries
- Record transactions with date, account code, particulars, debit, and credit
- Filter entries by date range
- Double-entry bookkeeping system

### 2. Chart of Accounts
- Create and manage account master data
- Support for different account types:
  - Assets
  - Liabilities
  - Equity
  - Income/Revenue
  - Expenses/Costs
- Delete accounts as needed

### 3. Ledger
- View account-wise transaction history
- Running balance calculation
- Filter by date range
- Detailed transaction particulars

### 4. Trial Balance
- Generate trial balance as of any date
- Automatic calculation of debit and credit balances
- Ensures books are balanced (Total Debit = Total Credit)
- Account-wise balance summary

### 5. Profit & Loss Account
- Generate P&L statement for any period
- Separate display of income and expenses
- Automatic calculation of net profit/loss
- Period comparison support

### 6. Data Import
- Import transactions from Excel files
- Compatible with "Final 2018-2025.xlsx" format
- Bulk data import capability

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory:**
   ```bash
   cd C:\Users\akosaraj\accounting-app
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

## Usage Guide

### Getting Started

1. **Setup Chart of Accounts:**
   - Go to "Chart of Accounts" tab
   - Add all your accounts with codes and types
   - Example: 
     - Code: 100, Name: "Madhavi Gari Investment", Type: "Equity"
     - Code: 101, Name: "Material Cost", Type: "Expense"

2. **Record Transactions:**
   - Go to "Daybook" tab
   - Add journal entries with date, account code, and amounts
   - For receipts: Enter amount in Debit
   - For payments: Enter amount in Credit

3. **View Ledger:**
   - Go to "Ledger" tab
   - Enter account code
   - Select date range (optional)
   - Click "Load Ledger" to view all transactions

4. **Generate Trial Balance:**
   - Go to "Trial Balance" tab
   - Select "As on Date"
   - Click "Generate Trial Balance"
   - Verify that Total Debit = Total Credit

5. **View Profit & Loss:**
   - Go to "Profit & Loss" tab
   - Select date range
   - Click "Generate P&L Statement"
   - View net profit or loss for the period

### Importing Existing Data

1. Go to "Import Data" tab
2. Click "Choose File" and select your Excel file
3. The system will read the "Daily Exp account wise" sheet
4. Click "Import Data"
5. Wait for confirmation message

## Technical Details

### Technology Stack
- **Backend:** Python Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Data Processing:** Pandas, OpenPyXL

### Database Schema

**accounts table:**
- id (Primary Key)
- account_code (Unique)
- account_name
- account_type
- created_at

**journal_entries table:**
- id (Primary Key)
- date
- account_code
- particulars
- debit
- credit
- created_at

### API Endpoints

- `GET/POST /api/accounts` - Manage accounts
- `DELETE /api/accounts/<code>` - Delete account
- `GET/POST /api/journal` - Manage journal entries
- `DELETE /api/journal/<id>` - Delete entry
- `GET /api/ledger/<code>` - Get account ledger
- `GET /api/trial-balance` - Generate trial balance
- `GET /api/profit-loss` - Generate P&L statement
- `POST /api/import-excel` - Import Excel data

## Account Types Guide

### Assets
Use for resources owned by the business:
- Cash, Bank accounts
- Accounts Receivable
- Inventory, Equipment

### Liabilities
Use for amounts owed:
- Accounts Payable
- Loans, Mortgages
- Accrued Expenses

### Equity
Use for owner's investment:
- Capital, Owner's Equity
- Retained Earnings
- Drawings

### Income/Revenue
Use for money earned:
- Sales Revenue
- Service Income
- Interest Income

### Expense/Cost
Use for money spent:
- Material Cost
- Salaries, Rent
- Utilities, Travel

## Tips for Best Results

1. **Consistent Account Codes:** Use a systematic numbering scheme
   - 100-199: Equity/Capital accounts
   - 200-299: Asset accounts
   - 300-399: Liability accounts
   - 400-499: Income accounts
   - 500-599: Expense accounts

2. **Regular Backups:** The database file `accounting_data.db` contains all your data. Back it up regularly.

3. **Date Format:** Use YYYY-MM-DD format for dates

4. **Double-Entry:** Every transaction affects at least two accounts. When you record a payment:
   - Debit the expense account
   - Credit the cash/bank account

5. **Verification:** Regularly generate Trial Balance to ensure books are balanced

## Troubleshooting

**Issue: Application won't start**
- Ensure Python 3.8+ is installed
- Install all requirements: `pip install -r requirements.txt`

**Issue: Data not showing**
- Check if you've added accounts in Chart of Accounts first
- Verify journal entries have valid account codes

**Issue: Import failed**
- Ensure Excel file format matches expected structure
- Check that account codes in Excel exist in Chart of Accounts

**Issue: Trial Balance not balanced**
- Review all journal entries for errors
- Ensure every debit has a corresponding credit

## Data Security

- Database is stored locally in `accounting_data.db`
- No data is sent to external servers
- Regular backups recommended
- Keep the application folder secure

## Future Enhancements

Potential features for future versions:
- Balance Sheet generation
- Cash Flow statement
- Multi-company support
- User authentication
- Export to PDF/Excel
- Advanced reporting and analytics
- Budget vs Actual comparison

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the usage guide
3. Verify your data format matches examples

## License

This application is provided as-is for accounting management purposes.
