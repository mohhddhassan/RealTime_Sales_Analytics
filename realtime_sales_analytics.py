from clickhouse_driver import Client, errors

try:
    # Connect to ClickHouse
    client = Client(host='localhost', database='retail_analytics')
    print("Connected to ClickHouse successfully.")

    # Check total rows in sales table
    try:
        total_rows = client.execute('SELECT count(*) FROM sales')
        print(f"\nTotal rows in sales table: {total_rows[0][0]}")
    except errors.Error as e:
        print(f"Error executing total row count query: {e}")

    # Query 1: Total revenue per category
    print("\n--- Total Revenue by Category ---")
    try:
        revenue_result = client.execute('''
            SELECT category, SUM(quantity * price) AS total_revenue
            FROM sales
            GROUP BY category
            ORDER BY total_revenue DESC
        ''')
        print(f"Revenue rows fetched: {len(revenue_result)}")
        for row in revenue_result:
            print(f"Category: {row[0]}, Revenue: ₹{row[1]:,.2f}")
    except errors.Error as e:
        print(f"Error executing total revenue query: {e}")

    # Query 2: Daily sales trend
    print("\n--- Daily Sales Trend ---")
    try:
        daily_sales = client.execute('''
            SELECT sale_date, SUM(quantity) AS total_items_sold
            FROM sales
            GROUP BY sale_date
            ORDER BY sale_date
        ''')
        print(f"Daily sales rows fetched: {len(daily_sales)}")
        for row in daily_sales:
            print(f"Date: {row[0]}, Items Sold: {row[1]}")
    except errors.Error as e:
        print(f"Error executing daily sales trend query: {e}")

    # Query 3: Top 3 products by revenue
    print("\n--- Top 3 Products by Revenue ---")
    try:
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
    except errors.Error as e:
        print(f"Error executing top products query: {e}")

except errors.NetworkError as ne:
    print(f"Network error while connecting to ClickHouse: {ne}")
except errors.ServerException as se:
    print(f"Server error from ClickHouse: {se}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
