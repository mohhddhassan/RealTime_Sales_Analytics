from clickhouse_driver import Client

# Connect to ClickHouse
client = Client(host='localhost', database='retail_analytics')

# Check total rows in sales table
total_rows = client.execute('SELECT count(*) FROM sales')
print(f"\nTotal rows in sales table: {total_rows[0][0]}")

# Query 1: Total revenue per category
print("\n--- Total Revenue by Category ---")
revenue_result = client.execute('''
    SELECT category, SUM(quantity * price) AS total_revenue
    FROM sales
    GROUP BY category
    ORDER BY total_revenue DESC
''')
print(f"Revenue rows fetched: {len(revenue_result)}")
for row in revenue_result:
    print(f"Category: {row[0]}, Revenue: ₹{row[1]:,.2f}")

# Query 2: Daily sales trend
print("\n--- Daily Sales Trend ---")
daily_sales = client.execute('''
    SELECT sale_date, SUM(quantity) AS total_items_sold
    FROM sales
    GROUP BY sale_date
    ORDER BY sale_date
''')
print(f"Daily sales rows fetched: {len(daily_sales)}")
for row in daily_sales:
    print(f"Date: {row[0]}, Items Sold: {row[1]}")

# Query 3: Top 3 products by revenue
print("\n--- Top 3 Products by Revenue ---")
top_products = client.execute('''
    SELECT product_name, SUM(quantity * price) AS revenue
    FROM sales
    GROUP BY product_name
    ORDER BY revenue DESC
    LIMIT 3
''')
print(f"Top products rows fetched: {len(top_products)}")
for row in top_products:
    print(f"Product: {row[0]}, Revenue: ₹{row[1]:,.2f}")
