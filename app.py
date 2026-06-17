from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine, text
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = 'accounting_data.db'
engine = create_engine(f'sqlite:///{DATA_FILE}')

def init_database():
    """Initialize database with required tables"""
    with engine.connect() as conn:
        # Journal entries table (Daybook)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        data = request.json
        with engine.connect() as conn:
            conn.execute(
                text("""INSERT INTO accounts (account_code, account_name, account_type)
                        VALUES (:code, :name, :type)"""),
                {
                    'code': data['account_code'],
                    'name': data['account_name'],
                    'type': data['account_type']
                }
            )
            conn.commit()
        return jsonify({'status': 'success'})

    # GET request
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM accounts ORDER BY account_code"))
        accounts = [dict(row._mapping) for row in result]
    return jsonify(accounts)

@app.route('/api/accounts/<account_code>', methods=['DELETE'])
def delete_account(account_code):
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM accounts WHERE account_code = :code"),
            {'code': account_code}
        )
        conn.commit()
    return jsonify({'status': 'success'})

@app.route('/api/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        data = request.json
        with engine.connect() as conn:
            conn.execute(
                text("""INSERT INTO journal_entries (date, account_code, particulars, debit, credit)
                        VALUES (:date, :account_code, :particulars, :debit, :credit)"""),
                {
                    'date': data['date'],
                    'account_code': data['account_code'],
                    'particulars': data['particulars'],
                    'debit': float(data.get('debit', 0)),
                    'credit': float(data.get('credit', 0))
                }
            )
            conn.commit()
        return jsonify({'status': 'success'})

    # GET request with optional date filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = "SELECT * FROM journal_entries WHERE 1=1"
    params = {}

    if start_date:
        query += " AND date >= :start_date"
        params['start_date'] = start_date
    if end_date:
        query += " AND date <= :end_date"
        params['end_date'] = end_date

    query += " ORDER BY date DESC, id DESC"

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        entries = [dict(row._mapping) for row in result]

    return jsonify(entries)

@app.route('/api/journal/<int:entry_id>', methods=['DELETE'])
def delete_journal_entry(entry_id):
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM journal_entries WHERE id = :id"),
            {'id': entry_id}
        )
        conn.commit()
    return jsonify({'status': 'success'})

@app.route('/api/ledger/<account_code>')
def ledger(account_code):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = """
        SELECT je.*, a.account_name
        FROM journal_entries je
        LEFT JOIN accounts a ON je.account_code = a.account_code
        WHERE je.account_code = :account_code
    """
    params = {'account_code': account_code}

    if start_date:
        query += " AND je.date >= :start_date"
        params['start_date'] = start_date
    if end_date:
        query += " AND je.date <= :end_date"
        params['end_date'] = end_date

    query += " ORDER BY je.date, je.id"

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        entries = [dict(row._mapping) for row in result]

    # Calculate running balance
    balance = 0
    for entry in entries:
        balance += entry['debit'] - entry['credit']
        entry['balance'] = balance

    return jsonify(entries)

@app.route('/api/trial-balance')
def trial_balance():
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))

    query = """
        SELECT
            a.account_code,
            a.account_name,
            a.account_type,
            COALESCE(SUM(je.debit), 0) as total_debit,
            COALESCE(SUM(je.credit), 0) as total_credit
        FROM accounts a
        LEFT JOIN journal_entries je ON a.account_code = je.account_code
            AND je.date <= :end_date
        GROUP BY a.account_code, a.account_name, a.account_type
        HAVING (total_debit - total_credit) != 0 OR total_debit > 0 OR total_credit > 0
        ORDER BY a.account_code
    """

    with engine.connect() as conn:
        result = conn.execute(text(query), {'end_date': end_date})
        accounts = []
        total_debit = 0
        total_credit = 0

        for row in result:
            row_dict = dict(row._mapping)
            balance = row_dict['total_debit'] - row_dict['total_credit']

            if balance > 0:
                row_dict['debit_balance'] = balance
                row_dict['credit_balance'] = 0
                total_debit += balance
            else:
                row_dict['debit_balance'] = 0
                row_dict['credit_balance'] = abs(balance)
                total_credit += abs(balance)

            accounts.append(row_dict)

    return jsonify({
        'accounts': accounts,
        'total_debit': total_debit,
        'total_credit': total_credit
    })

@app.route('/api/profit-loss')
def profit_loss():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))

    query = """
        SELECT
            a.account_code,
            a.account_name,
            a.account_type,
            COALESCE(SUM(je.debit), 0) as total_debit,
            COALESCE(SUM(je.credit), 0) as total_credit
        FROM accounts a
        LEFT JOIN journal_entries je ON a.account_code = je.account_code
            AND je.date <= :end_date
    """
    params = {'end_date': end_date}

    if start_date:
        query += " AND je.date >= :start_date"
        params['start_date'] = start_date

    query += """
        WHERE a.account_type IN ('Income', 'Expense', 'Revenue', 'Cost')
        GROUP BY a.account_code, a.account_name, a.account_type
        ORDER BY a.account_type, a.account_code
    """

    with engine.connect() as conn:
        result = conn.execute(text(query), params)

        income_accounts = []
        expense_accounts = []
        total_income = 0
        total_expenses = 0

        for row in result:
            row_dict = dict(row._mapping)
            balance = row_dict['total_credit'] - row_dict['total_debit']
            row_dict['amount'] = abs(balance)

            if row_dict['account_type'] in ['Income', 'Revenue']:
                income_accounts.append(row_dict)
                total_income += row_dict['amount'] if balance > 0 else -row_dict['amount']
            elif row_dict['account_type'] in ['Expense', 'Cost']:
                expense_accounts.append(row_dict)
                total_expenses += row_dict['amount'] if balance < 0 else -row_dict['amount']

    net_profit = total_income - total_expenses

    return jsonify({
        'income': income_accounts,
        'expenses': expense_accounts,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_profit': net_profit
    })

@app.route('/api/import-excel', methods=['POST'])
def import_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        xl = pd.ExcelFile(file)
        imported_count = 0

        with engine.connect() as conn:
            # Import from Daily Exp account wise sheet
            if 'Daily Exp account wise' in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name='Daily Exp account wise', skiprows=1)

                for _, row in df.iterrows():
                    if pd.notna(row.get('A/c Code')) and pd.notna(row.get('Date')):
                        account_code = str(int(row['A/c Code']))
                        date = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
                        particulars = str(row.get('Particulars', ''))
                        debit = float(row.get('Cash In', 0)) if pd.notna(row.get('Cash In')) else 0
                        credit = float(row.get('Cash out', 0)) if pd.notna(row.get('Cash out')) else 0

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

            conn.commit()

        return jsonify({
            'status': 'success',
            'imported_count': imported_count
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
