import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("expense.db")
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON;")

cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    merchant VARCHAR(100),
    payment_method VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT positive_amount CHECK (amount > 0)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(50) NOT NULL UNIQUE,
    monthly_limit DECIMAL(10, 2) NOT NULL,
    CONSTRAINT positive_limit CHECK (monthly_limit > 0)
);
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category);")

cur.execute("""
CREATE VIEW IF NOT EXISTS v_monthly_summary AS
SELECT 
    strftime('%Y-%m', date) AS month,
    COUNT(*) AS transactions,
    SUM(amount) AS total,
    AVG(amount) AS avg_transaction,
    SUM(SUM(amount)) OVER (ORDER BY strftime('%Y-%m', date)) AS running_total
FROM expenses
GROUP BY month
ORDER BY month;
""")

cur.execute("""
CREATE VIEW IF NOT EXISTS v_category_summary AS
SELECT 
    category,
    COUNT(*) AS transactions,
    SUM(amount) AS total,
    AVG(amount) AS avg_amount,
    ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM expenses), 2) AS percentage
FROM expenses
GROUP BY category
ORDER BY total DESC;
""")

default_budgets = [
    ('Groceries', 600.00),
    ('Dining', 300.00),
    ('Transportation', 200.00),
    ('Entertainment', 150.00),
    ('Shopping', 250.00),
]

cur.executemany("INSERT OR IGNORE INTO budgets (category, monthly_limit) VALUES (?, ?)", default_budgets)

response = input("Generate sample data? (y/n): ").lower()

if response == 'y':
    categories = {
        'Groceries': ['Whole Foods', 'Safeway', 'Trader Joes'],
        'Dining': ['Chipotle', 'Local Cafe', 'Pizza Place'],
        'Transportation': ['Shell Gas', 'Uber', 'Metro'],
        'Entertainment': ['Netflix', 'Movie Theater', 'Steam'],
        'Shopping': ['Amazon', 'Target', 'Best Buy'],
    }
    
    start_date = datetime.now() - timedelta(days=180)
    expenses = []
    
    for day in range(180):
        current_date = start_date + timedelta(days=day)
        for _ in range(random.randint(1, 3)):
            category = random.choice(list(categories.keys()))
            merchant = random.choice(categories[category])
            amount = round(random.uniform(10.00, 150.00), 2)
            
            expenses.append((
                current_date.strftime('%Y-%m-%d'),
                category,
                amount,
                merchant,
                random.choice(['cash', 'debit', 'credit'])
            ))
    
    cur.executemany("""
    INSERT INTO expenses (date, category, amount, merchant, payment_method)
    VALUES (?, ?, ?, ?, ?)
    """, expenses)
    
    print(f"✓ Created {len(expenses)} sample expenses")

conn.commit()
conn.close()
print("✓ Database initialized")
