import sqlite3

conn = sqlite3.connect("expense.db")
cur = conn.cursor()

print("\nADVANCED EXPENSE ANALYTICS\n")

print("=" * 80)
print("CATEGORY ANALYSIS")
print("=" * 80)

cur.execute("""
SELECT 
    category,
    COUNT(*) AS txn_count,
    SUM(amount) AS total,
    AVG(amount) AS avg,
    ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM expenses), 2) AS pct,
    RANK() OVER (ORDER BY SUM(amount) DESC) AS rank,
    SUM(SUM(amount)) OVER (ORDER BY SUM(amount) DESC) * 100.0 / 
        (SELECT SUM(amount) FROM expenses) AS cumulative_pct
FROM expenses
GROUP BY category
ORDER BY total DESC;
""")

print(f"\n{'Category':<15} {'Total':<12} {'Txns':<6} {'Avg':<10} {'%':<6} {'Rank':<5} {'Cum%':<6}")
print("-" * 70)

for cat, count, total, avg, pct, rank, cum_pct in cur.fetchall():
    print(f"{cat:<15} ${total:>10,.2f} {count:>5} ${avg:>8,.2f} {pct:>5.1f} {rank:>4} {cum_pct:>5.1f}")

print("\n" + "=" * 80)
print("TREND ANALYSIS")
print("=" * 80)

cur.execute("""
WITH daily_spending AS (
    SELECT 
        date,
        SUM(amount) AS daily_total
    FROM expenses
    GROUP BY date
)
SELECT 
    date,
    daily_total,
    AVG(daily_total) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7,
    AVG(daily_total) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS ma_30
FROM daily_spending
ORDER BY date DESC
LIMIT 30;
""")

print(f"\n{'Date':<12} {'Daily':<10} {'7D MA':<10} {'30D MA':<10}")
print("-" * 50)

for date, daily, ma7, ma30 in cur.fetchall():
    print(f"{date:<12} ${daily:>8,.2f} ${ma7:>8,.2f} ${ma30:>8,.2f}")

print("\n" + "=" * 80)
print("BUDGET VS ACTUAL (Current Month)")
print("=" * 80)

cur.execute("""
SELECT 
    b.category,
    b.monthly_limit,
    COALESCE(SUM(e.amount), 0) AS actual,
    b.monthly_limit - COALESCE(SUM(e.amount), 0) AS remaining,
    ROUND(COALESCE(SUM(e.amount), 0) * 100.0 / b.monthly_limit, 1) AS pct_used
FROM budgets b
LEFT JOIN expenses e ON b.category = e.category 
    AND strftime('%Y-%m', e.date) = strftime('%Y-%m', 'now')
GROUP BY b.category, b.monthly_limit
ORDER BY pct_used DESC;
""")

print(f"\n{'Category':<15} {'Budget':<12} {'Spent':<12} {'Remaining':<12} {'Used%':<8}")
print("-" * 60)

for cat, budget, actual, remaining, pct in cur.fetchall():
    status = "⚠️" if pct > 80 else "✓"
    print(f"{cat:<15} ${budget:>10,.2f} ${actual:>10,.2f} ${remaining:>10,.2f} {pct:>6.1f}% {status}")

print("\n" + "=" * 80)
print("SPENDING PATTERNS")
print("=" * 80)

cur.execute("""
SELECT 
    CASE CAST(strftime('%w', date) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day,
    COUNT(*) AS txns,
    SUM(amount) AS total,
    AVG(amount) AS avg
FROM expenses
GROUP BY strftime('%w', date)
ORDER BY CAST(strftime('%w', date) AS INTEGER);
""")

print(f"\n{'Day':<12} {'Transactions':<15} {'Total':<12} {'Average':<10}")
print("-" * 55)

for day, txns, total, avg in cur.fetchall():
    print(f"{day:<12} {txns:<15} ${total:>10,.2f} ${avg:>8,.2f}")

print("\n" + "=" * 80)
print("TOP MERCHANTS")
print("=" * 80)

cur.execute("""
SELECT 
    merchant,
    category,
    COUNT(*) AS visits,
    SUM(amount) AS total,
    AVG(amount) AS avg_per_visit
FROM expenses
WHERE merchant IS NOT NULL
GROUP BY merchant, category
ORDER BY total DESC
LIMIT 10;
""")

print(f"\n{'Merchant':<20} {'Category':<15} {'Visits':<8} {'Total':<12} {'Avg':<10}")
print("-" * 70)

for merchant, cat, visits, total, avg in cur.fetchall():
    print(f"{merchant:<20} {cat:<15} {visits:<8} ${total:>10,.2f} ${avg:>8,.2f}")

conn.close()
