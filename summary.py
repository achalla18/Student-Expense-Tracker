import sqlite3

conn = sqlite3.connect("expense.db")
cur = conn.cursor()

print("\nMONTHLY EXPENSE SUMMARY\n")
print(f"{'Month':<10} {'Total':<12} {'Txns':<6} {'Avg':<10} {'Running':<12} {'vs Prev':<10}")
print("-" * 70)

cur.execute("""
WITH monthly_data AS (
    SELECT 
        strftime('%Y-%m', date) AS month,
        SUM(amount) AS total,
        COUNT(*) AS txn_count,
        AVG(amount) AS avg_txn
    FROM expenses
    GROUP BY month
)
SELECT 
    month,
    total,
    txn_count,
    avg_txn,
    SUM(total) OVER (ORDER BY month) AS running_total,
    total - LAG(total, 1) OVER (ORDER BY month) AS mom_change,
    ROUND((total - LAG(total, 1) OVER (ORDER BY month)) * 100.0 / 
          LAG(total, 1) OVER (ORDER BY month), 1) AS pct_change
FROM monthly_data
ORDER BY month;
""")

for month, total, txn, avg, running, change, pct in cur.fetchall():
    change_str = f"+${change:.2f}" if change and change > 0 else f"${change:.2f}" if change else "N/A"
    pct_str = f"({pct:+.1f}%)" if pct else ""
    print(f"{month:<10} ${total:>10,.2f} {txn:>5} ${avg:>8,.2f} ${running:>10,.2f} {change_str:>8} {pct_str}")

cur.execute("SELECT SUM(amount), AVG(amount), COUNT(*) FROM expenses")
total, avg, count = cur.fetchone()

print("-" * 70)
print(f"\nTotal Spent: ${total:,.2f}")
print(f"Avg Transaction: ${avg:.2f}")
print(f"Total Transactions: {count}")

conn.close()
