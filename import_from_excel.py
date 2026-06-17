"""
Standalone script to import data from Excel file directly to database
This can be run independently of the web application
"""

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_FILE = 'accounting_data.db'
engine = create_engine(f'sqlite:///{DATA_FILE}')

def init_database():
    """Initialize database if it doesn't exist"""
    with engine.connect() as conn:
        # Journal entries table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                account_code TEXT NOT NULL,
                particulars TEXT NOT NULL,
                debit REAL DEFAULT 0,
                credit REAL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """))

        # Accounts master table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_code TEXT UNIQUE NOT NULL,
                account_name TEXT NOT NULL,
                account_type TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.commit()
    print("✓ Database initialized")

def import_excel_file(file_path):
    """Import data from Excel file"""
    print(f"\nReading Excel file: {file_path}")

    try:
        xl = pd.ExcelFile(file_path)
        print(f"✓ Found {len(xl.sheet_names)} sheets")

        imported_count = 0
        skipped_count = 0

        # Import from Daily Exp account wise sheet
        if 'Daily Exp account wise' in xl.sheet_names:
            print("\nProcessing 'Daily Exp account wise' sheet...")
            df = pd.read_excel(xl, sheet_name='Daily Exp account wise', skiprows=1)

            print(f"Total rows to process: {len(df)}")

            # Determine column indices dynamically
            col_account = df.columns[0]  # First column is account code
            col_date = df.columns[1]      # Second column is date
            col_particulars = df.columns[2]  # Third column is particulars
            col_debit = df.columns[3]     # Fourth column is cash in (debit)
            col_credit = df.columns[4]    # Fifth column is cash out (credit)

            with engine.connect() as conn:
                for idx, row in df.iterrows():
                    if pd.notna(row[col_account]) and pd.notna(row[col_date]):
                        try:
                            account_code = str(int(row[col_account]))
                            date = pd.to_datetime(row[col_date]).strftime('%Y-%m-%d')
                            particulars = str(row[col_particulars]) if pd.notna(row[col_particulars]) else 'N/A'

                            # Get debit and credit amounts
                            debit = float(row[col_debit]) if pd.notna(row[col_debit]) else 0
                            credit = float(row[col_credit]) if pd.notna(row[col_credit]) else 0

                            if debit > 0 or credit > 0:
                                conn.execute(
                                    text("""INSERT INTO journal_entries
                                            (date, account_code, particulars, debit, credit)
                                            VALUES (:date, :code, :part, :debit, :credit)"""),
                                    {
                                        'date': date,
                                        'code': account_code,
                                        'part': particulars,
                                        'debit': debit,
                                        'credit': credit
                                    }
                                )
                                imported_count += 1

                                if imported_count % 100 == 0:
                                    print(f"  Imported {imported_count} entries...")
                            else:
                                skipped_count += 1

                        except Exception as e:
                            print(f"  Error processing row {idx + 2}: {e}")
                            skipped_count += 1

                conn.commit()

            print(f"\n✓ Import complete!")
            print(f"  - Successfully imported: {imported_count} entries")
            print(f"  - Skipped (no amount): {skipped_count} entries")

        else:
            print("✗ Sheet 'Daily Exp account wise' not found")
            print("Available sheets:", xl.sheet_names)

    except FileNotFoundError:
        print(f"✗ Error: File not found: {file_path}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def create_sample_accounts():
    """Create sample accounts based on common account codes"""
    print("\nCreating sample accounts...")

    sample_accounts = [
        ('100', 'Madhavi Gari Investment', 'Equity'),
        ('101', 'Owner Capital', 'Equity'),
        ('102', 'Funds Receipt from Abroad', 'Equity'),
        ('103', 'Partner Investment', 'Equity'),
        ('108', 'Additional Capital', 'Equity'),
        ('111', 'Mirchi Investment', 'Asset'),
        ('115', 'Shankar Account', 'Asset'),
        ('200', 'Cash in Hand', 'Asset'),
        ('201', 'Bank Account', 'Asset'),
        ('500', 'Material Cost', 'Expense'),
        ('501', 'C&F Charges', 'Expense'),
        ('502', 'Marking & Loading Charges', 'Expense'),
        ('503', 'Bank Charges', 'Expense'),
        ('504', 'Taxes and Duties', 'Expense'),
        ('505', 'Machinery & Polish Material', 'Expense'),
        ('506', 'Travelling Expenses', 'Expense'),
    ]

    with engine.connect() as conn:
        for code, name, acc_type in sample_accounts:
            try:
                conn.execute(
                    text("""INSERT OR IGNORE INTO accounts
                            (account_code, account_name, account_type)
                            VALUES (:code, :name, :type)"""),
                    {'code': code, 'name': name, 'type': acc_type}
                )
            except Exception as e:
                pass  # Ignore duplicates

        conn.commit()

    print("✓ Sample accounts created")

if __name__ == '__main__':
    print("=" * 60)
    print("  Excel Data Import Tool - Accounting System")
    print("=" * 60)

    # Initialize database
    init_database()

    # Create sample accounts
    create_sample_accounts()

    # Get file path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Default path
        file_path = r'C:\Users\akosaraj\Downloads\Final 2018-2025.xlsx'
        print(f"\nUsing default file path: {file_path}")
        print("(You can also run: python import_from_excel.py <your_file_path>)")

    # Import data
    import_excel_file(file_path)

    print("\n" + "=" * 60)
    print("Import process completed!")
    print("You can now start the web application with: python app.py")
    print("=" * 60)
