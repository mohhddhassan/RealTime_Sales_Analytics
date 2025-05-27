import streamlit as st
import pandas as pd
import altair as alt
from clickhouse_driver import Client
from datetime import datetime

# Connect to ClickHouse
client = Client(host='localhost', database='retail_analytics')

# Streamlit page config
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

st.title("📊 Real-Time Sales Analytics Dashboard")
st.markdown("""
Welcome to your live sales insights. Use the filters below to explore sales performance by category, date, and products.
""")

# Date filter
min_date = client.execute('SELECT MIN(sale_date) FROM sales')[0][0]
max_date = client.execute('SELECT MAX(sale_date) FROM sales')[0][0]

start_date, end_date = st.date_input(
    "Select Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if start_date > end_date:
    st.error("Error: Start date must be before end date.")
    st.stop()

# Helper function to fetch data with date filter


def fetch_data(query):
    return client.execute(query, {'start_date': start_date, 'end_date': end_date})


# KPIs
total_revenue_query = '''
    SELECT SUM(quantity * price) FROM sales
    WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
'''
total_quantity_query = '''
    SELECT SUM(quantity) FROM sales
    WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
'''
avg_price_query = '''
    SELECT AVG(price) FROM sales
    WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
'''

total_revenue = fetch_data(total_revenue_query)[0][0] or 0
total_quantity = fetch_data(total_quantity_query)[0][0] or 0
avg_price = fetch_data(avg_price_query)[0][0] or 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Total Items Sold", f"{total_quantity:,}")
col3.metric("Average Price", f"₹{avg_price:,.2f}")

# Revenue by Category
category_query = '''
    SELECT category, SUM(quantity * price) AS total_revenue
    FROM sales
    WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
    GROUP BY category
    ORDER BY total_revenue DESC
'''
category_data = fetch_data(category_query)
df_category = pd.DataFrame(category_data, columns=[
                           'Category', 'Total Revenue'])

st.markdown("### 💰 Total Revenue by Category")
chart_category = alt.Chart(df_category).mark_bar().encode(
    x=alt.X('Category:N', axis=alt.Axis(labelAngle=-45,
            labelFontSize=14, titleFontSize=16)),  # Increased font sizes
    y=alt.Y('Total Revenue:Q', axis=alt.Axis(
        labelFontSize=14, titleFontSize=16)),
    tooltip=['Category', 'Total Revenue']
).properties(width=600, height=400).configure_axis(
    titleFontSize=16,
    labelFontSize=14
)
st.altair_chart(chart_category, use_container_width=True)

# Top products by revenue
top_products_query = '''
    SELECT product_name, SUM(quantity * price) AS revenue
    FROM sales
    WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
    GROUP BY product_name
    ORDER BY revenue DESC
    LIMIT 5
'''
top_products_data = fetch_data(top_products_query)
df_top_products = pd.DataFrame(
    top_products_data, columns=['Product', 'Revenue'])

st.markdown("### 🏆 Top 5 Products by Revenue")
chart_products = alt.Chart(df_top_products).mark_bar().encode(
    x=alt.X('Product:N', axis=alt.Axis(labelAngle=-45,
            labelFontSize=14, titleFontSize=16)),  # Increased font sizes
    y=alt.Y('Revenue:Q', axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
    tooltip=['Product', 'Revenue']
).properties(width=600, height=400).configure_axis(
    titleFontSize=16,
    labelFontSize=14
)
st.altair_chart(chart_products, use_container_width=True)

# Daily sales trend
daily_sales_query = '''
    SELECT sale_date, SUM(quantity) AS total_items_sold
    FROM sales
    WHERE sale_date BETWEEN %(start_date)s AND %(end_date)s
    GROUP BY sale_date
    ORDER BY sale_date
'''
daily_sales_data = fetch_data(daily_sales_query)
df_daily_sales = pd.DataFrame(daily_sales_data, columns=[
                              'Sale Date', 'Items Sold'])
df_daily_sales['Sale Date'] = pd.to_datetime(df_daily_sales['Sale Date'])

st.markdown("### 📅 Daily Sales Trend")
st.line_chart(df_daily_sales.rename(
    columns={"Sale Date": "index"}).set_index('index'))

# Optional raw data viewer
with st.expander("See Raw Data (Category Revenue)"):
    st.dataframe(df_category)

# Footer timestamp
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
