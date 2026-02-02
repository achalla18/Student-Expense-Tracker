import sqlite3

conn = sqlite3.connect("expense.db")
cur = conn.cursor()

print("\nMonthly Expense Totals:\n")

cur.execute("""
SELECT 
    strftime('%Y-%m', date) AS month,
    SUM(amount)
FROM expenses
GROUP BY month
ORDER BY month;
""")

rows = cur.fetchall()

for month, total in rows:
    print(f"{month}: ${total:.2f}")

conn.close()
