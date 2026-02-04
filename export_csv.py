import sqlite3
import pandas as pd

conn = sqlite3.connect("expense.db")

print("\n1. Category Summary")
print("2. Monthly Breakdown")
print("3. All Transactions")

choice = input("\nExport option: ")

if choice == '1':
    query = """
    SELECT 
        category,
        COUNT(*) AS transactions,
        SUM(amount) AS total,
        AVG(amount) AS avg_amount,
        MIN(amount) AS min_amount,
        MAX(amount) AS max_amount,
        ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM expenses), 2) AS percentage
    FROM expenses
    GROUP BY category
    ORDER BY total DESC;
    """
    df = pd.read_sql(query, conn)
    filename = "category_summary.csv"

elif choice == '2':
    query = """
    SELECT 
        strftime('%Y-%m', date) AS month,
        category,
        SUM(amount) AS total,
        COUNT(*) AS transactions,
        AVG(amount) AS avg_amount
    FROM expenses
    GROUP BY month, category
    ORDER BY month DESC, total DESC;
    """
    df = pd.read_sql(query, conn)
    filename = "monthly_breakdown.csv"

elif choice == '3':
    query = """
    SELECT 
        id,
        date,
        category,
        amount,
        description,
        merchant,
        payment_method
    FROM expenses
    ORDER BY date DESC;
    """
    df = pd.read_sql(query, conn)
    filename = "all_transactions.csv"

else:
    print("Invalid choice")
    conn.close()
    exit()

df.to_csv(filename, index=False)
print(f"✓ Exported to {filename}")

conn.close()
