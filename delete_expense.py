import sqlite3

conn = sqlite3.connect("expense.db")
cur = conn.cursor()

expense_id = int(input("Enter expense ID to delete: "))

cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

conn.commit()
conn.close()

print("Expense deleted.")
