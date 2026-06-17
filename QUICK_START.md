# Quick Start Guide

## Your Accounting Application is Ready!

Your data from "Final 2018-2025.xlsx" has been successfully imported.

### Imported Data Summary
- **2,957 journal entries** imported from your Excel file
- **Sample accounts** created for common account codes (100, 101, 102, 103, 108, 111, 115, etc.)

## How to Start the Application

### Option 1: Using the Batch File (Easiest)
1. Double-click `start.bat` in the accounting-app folder
2. Wait for the application to start
3. Open your browser to: **http://localhost:5000**

### Option 2: Manual Start
1. Open Command Prompt or PowerShell
2. Navigate to: `cd C:\Users\akosaraj\accounting-app`
3. Run: `python app.py`
4. Open your browser to: **http://localhost:5000**

## Application URL
```
http://localhost:5000
```

## What You Can Do Now

### 1. View Your Daybook
- Click on the **"Daybook"** tab
- See all 2,957 imported transactions
- Filter by date range
- Add new entries

### 2. Check Chart of Accounts
- Click on the **"Chart of Accounts"** tab
- View all your account codes and names
- Add new accounts as needed
- Edit account types (Asset, Liability, Income, Expense, etc.)

### 3. View Account Ledgers
- Click on the **"Ledger"** tab
- Enter an account code (e.g., 100, 101, 103)
- See all transactions for that account with running balance
- Filter by date range

### 4. Generate Trial Balance
- Click on the **"Trial Balance"** tab
- Select an "as on" date
- Click "Generate Trial Balance"
- Verify that Total Debit = Total Credit

### 5. View Profit & Loss
- Click on the **"Profit & Loss"** tab
- Select date range
- Click "Generate P&L Statement"
- See income vs expenses and net profit/loss

## Your Account Codes

Based on your imported data, here are some common account codes:

- **100** - Madhavi Gari Investment (Equity)
- **101** - Owner Capital (Equity)
- **102** - Funds Receipt from Abroad (Equity)
- **103** - Partner Investment (Equity)
- **108** - Additional Capital (Equity)
- **111** - Mirchi Investment (Asset)
- **115** - Shankar Account (Asset)
- **200** - Cash in Hand (Asset)
- **201** - Bank Account (Asset)
- **500-599** - Various Expenses

## Tips for Using the Application

1. **Adding New Entries:**
   - Always use existing account codes
   - Either Debit OR Credit should be filled (not both)
   - Receipts = Debit, Payments = Credit

2. **Creating New Accounts:**
   - Go to Chart of Accounts
   - Add account code, name, and type
   - Then you can use it in journal entries

3. **Viewing Reports:**
   - Trial Balance: Shows all account balances
   - Profit & Loss: Shows only Income and Expense accounts
   - Ledger: Shows transactions for one specific account

4. **Date Formats:**
   - Use YYYY-MM-DD format (e.g., 2025-06-17)
   - The system will accept standard date picker formats

## Stopping the Application

- Press **Ctrl + C** in the Command Prompt/Terminal window
- Or simply close the window

## Troubleshooting

**Issue: Application won't start**
- Make sure Python is installed
- Run: `pip install flask flask-cors sqlalchemy openpyxl`

**Issue: Can't see data**
- Data is stored in `accounting_data.db` file
- If needed, re-import: `python import_from_excel.py`

**Issue: Port already in use**
- Another application might be using port 5000
- Edit `app.py` and change the port number

## File Locations

- **Database:** `accounting_data.db` (contains all your data)
- **Application:** `app.py`
- **Import Tool:** `import_from_excel.py`
- **Excel File:** `C:\Users\akosaraj\Downloads\Final 2018-2025.xlsx`

## Backup Your Data

Your accounting data is stored in the file:
```
C:\Users\akosaraj\accounting-app\accounting_data.db
```

**Important:** Regularly backup this file to prevent data loss!

## Next Steps

1. **Review Imported Data:**
   - Check if all entries were imported correctly
   - Verify account codes match your expectations

2. **Update Account Types:**
   - Go to Chart of Accounts
   - Make sure each account has the correct type
   - This affects Profit & Loss calculations

3. **Generate Reports:**
   - Create a Trial Balance for the latest date
   - Generate P&L for different periods
   - Review ledgers for key accounts

4. **Add New Transactions:**
   - Start recording new transactions in Daybook
   - Keep your accounting up to date

## Need Help?

- Check the main **README.md** file for detailed documentation
- Review the **Usage Guide** section
- Look at the **API Endpoints** for technical details

---

**Application Created:** June 17, 2026
**Data Imported:** 2,957 entries from Final 2018-2025.xlsx
**Status:** Ready to use!
