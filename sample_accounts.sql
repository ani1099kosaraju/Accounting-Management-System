-- Sample Chart of Accounts
-- Run this to populate your database with common accounts

-- Capital/Equity Accounts (100 series)
INSERT INTO accounts (account_code, account_name, account_type) VALUES
('100', 'Madhavi Gari Investment', 'Equity'),
('101', 'Owner Capital', 'Equity'),
('102', 'Funds Receipt from Abroad', 'Equity');

-- Asset Accounts (200 series)
INSERT INTO accounts (account_code, account_name, account_type) VALUES
('200', 'Cash in Hand', 'Asset'),
('201', 'KVB Bank Account', 'Asset'),
('202', 'Central Bank Account', 'Asset'),
('203', 'IDFC Bank Account', 'Asset'),
('204', 'Accounts Receivable', 'Asset');

-- Expense Accounts (500 series)
INSERT INTO accounts (account_code, account_name, account_type) VALUES
('500', 'Material Cost', 'Expense'),
('501', 'C&F Charges', 'Expense'),
('502', 'Marking & Loading Charges', 'Expense'),
('503', 'Bank Charges', 'Expense'),
('504', 'Taxes and Duties', 'Expense'),
('505', 'Cutting Machinery & Polish Material', 'Expense'),
('506', 'Travelling Expenses', 'Expense'),
('507', 'Salary Expenses', 'Expense'),
('508', 'Rent Expenses', 'Expense'),
('509', 'Utilities', 'Expense');

-- Income/Revenue Accounts (400 series)
INSERT INTO accounts (account_code, account_name, account_type) VALUES
('400', 'Sales Revenue', 'Income'),
('401', 'Service Income', 'Income'),
('402', 'Interest Income', 'Income');

-- Liability Accounts (300 series)
INSERT INTO accounts (account_code, account_name, account_type) VALUES
('300', 'Accounts Payable', 'Liability'),
('301', 'Loans Payable', 'Liability'),
('302', 'Interest on Loans', 'Liability');

-- Investment Accounts (110 series)
INSERT INTO accounts (account_code, account_name, account_type) VALUES
('111', 'Mirchi Investment', 'Asset'),
('115', 'Shankar Account', 'Asset');
