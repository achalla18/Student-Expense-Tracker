import sqlite3
import pandas as pd

conn = sqlite3.connect("expense.db")

query = """
SELECT 
    category,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY category;
"""

df = pd.read_sql(query, conn)
df.to_csv("expense_summary.csv", index=False)

conn.close()

print("Exported to expense_summary.csv")
