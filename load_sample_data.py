"""
Utility script to load sample accounts into the database
Run this after starting the application for the first time
"""

from sqlalchemy import create_engine, text

DATA_FILE = 'accounting_data.db'
engine = create_engine(f'sqlite:///{DATA_FILE}')

def load_sample_accounts():
    """Load sample accounts from SQL file"""
    try:
        with open('sample_accounts.sql', 'r') as f:
            sql_content = f.read()

        # Split by semicolon and execute each statement
        statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]

        with engine.connect() as conn:
            for statement in statements:
                if statement:
                    try:
                        conn.execute(text(statement))
                        print(f"✓ Executed: {statement[:50]}...")
                    except Exception as e:
                        print(f"✗ Error: {e}")

            conn.commit()

        print("\n✓ Sample accounts loaded successfully!")
        print("You can now start adding journal entries.")

    except FileNotFoundError:
        print("Error: sample_accounts.sql file not found")
    except Exception as e:
        print(f"Error loading sample data: {e}")

if __name__ == '__main__':
    print("Loading sample accounts...")
    print("-" * 50)
    load_sample_accounts()
