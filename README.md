# Expense Tracker

A Python-based expense tracking system with advanced SQL analytics.

## Features

- Monthly expense summaries with trend analysis
- Category breakdowns with rankings
- Budget vs actual monitoring
- CSV export capabilities
- Advanced SQL queries 


## Setup

```bash
# Initialize database (generates sample data if needed)
python init_database.py

# View analytics
python analytics.py
python summary.py
```

## Database Schema

**Tables:**
- `expenses` - Transaction records
- `budgets` - Monthly budget limits by category

**Views:**
- `v_monthly_summary` - Monthly totals with running sums
- `v_category_summary` - Category breakdowns with percentages

**Indexes:**
- `idx_expenses_date` - Date lookup optimization
- `idx_expenses_category` - Category filtering optimization

## SQL Features

### Window Functions
```sql
SUM(amount) OVER (ORDER BY date) AS running_total
LAG(total) OVER (ORDER BY month) AS previous_month
RANK() OVER (ORDER BY total DESC) AS rank
```

### Common Table Expressions (CTEs)
```sql
WITH monthly_data AS (
    SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total
    FROM expenses GROUP BY month
)
SELECT * FROM monthly_data;
```

### Views with Aggregations
```sql
CREATE VIEW v_monthly_summary AS
SELECT 
    strftime('%Y-%m', date) AS month,
    SUM(amount) AS total,
    SUM(SUM(amount)) OVER (ORDER BY month) AS running_total
FROM expenses GROUP BY month;
```

## Usage Examples

**Add expense:**
```python
import sqlite3
conn = sqlite3.connect("expense.db")
cur = conn.cursor()
cur.execute("INSERT INTO expenses (date, category, amount) VALUES ('2026-02-03', 'Groceries', 45.50)")
conn.commit()
```

**View monthly summary:**
```bash
python summary.py
```

**Export category data:**
```bash
python export_csv.py
# Select option 1
```

**Run analytics:**
```bash
python analytics.py
```

## Analytics Output

The `analytics.py` script provides:
- Category rankings with cumulative percentages
- 7-day and 30-day moving averages
- Budget vs actual comparisons
- Spending patterns by day of week
- Top merchants by total spend

## Requirements

```bash
pip install pandas
```

---
