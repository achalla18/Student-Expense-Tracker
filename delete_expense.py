import sqlite3

conn = sqlite3.connect("expense.db")
cur = conn.cursor()

print("\n1. Delete by ID")
print("2. Delete by category")
print("3. View recent expenses")

choice = input("\nOption: ")

if choice == '1':
    expense_id = int(input("Enter expense ID: "))
    
    cur.execute("SELECT date, category, amount, description FROM expenses WHERE id = ?", (expense_id,))
    expense = cur.fetchone()
    
    if expense:
        print(f"\nDate: {expense[0]}, Category: {expense[1]}, Amount: ${expense[2]:.2f}")
        confirm = input("Delete this expense? (yes/no): ")
        
        if confirm.lower() == 'yes':
            cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
            print("✓ Expense deleted")
        else:
            print("Cancelled")
    else:
        print("Expense not found")

elif choice == '2':
    cur.execute("SELECT category, COUNT(*), SUM(amount) FROM expenses GROUP BY category ORDER BY category")
    categories = cur.fetchall()
    
    print("\nCategories:")
    for cat, count, total in categories:
        print(f"  {cat}: {count} transactions, ${total:.2f}")
    
    category = input("\nEnter category to delete: ")
    
    cur.execute("SELECT COUNT(*), SUM(amount) FROM expenses WHERE category = ?", (category,))
    count, total = cur.fetchone()
    
    if count > 0:
        print(f"\nWARNING: Deleting {count} expenses totaling ${total:.2f}")
        confirm = input(f"Type 'DELETE {category}' to confirm: ")
        
        if confirm == f'DELETE {category}':
            cur.execute("DELETE FROM expenses WHERE category = ?", (category,))
            conn.commit()
            print(f"✓ Deleted {count} expenses")
        else:
            print("Cancelled")
    else:
        print("No expenses found")

elif choice == '3':
    cur.execute("""
    SELECT id, date, category, amount, merchant 
    FROM expenses 
    ORDER BY date DESC 
    LIMIT 20
    """)
    
    print(f"\n{'ID':<6} {'Date':<12} {'Category':<15} {'Amount':<10} {'Merchant':<20}")
    print("-" * 70)
    
    for row in cur.fetchall():
        print(f"{row[0]:<6} {row[1]:<12} {row[2]:<15} ${row[3]:>8,.2f} {row[4] or '':<20}")

else:
    print("Invalid option")

conn.close()
