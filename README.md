# 📊 Realtime Sales Analytics Dashboard

This project is a real-time retail sales analytics dashboard built using **Python**, **ClickHouse**, and **Streamlit**. It provides interactive insights into sales data including KPIs, revenue by category, top products, and daily trends.

### 🔍 Dashboard Previews

- [Dashboard-preview-1](assets/Dashboard-preview-1.png)
- [Dashboard-preview-2](assets/Dashboard-preview-2.png)
- [Dashboard-preview-3](assets/Dashboard-preview-3.png)

---

## 🚀 Features

- 📅 Date range filter with dynamic query support
- 📈 Revenue and quantity KPIs
- 💰 Revenue breakdown by category
- 🏆 Top 5 products by revenue
- 📊 Daily sales trend chart
- 📷 Slanted axis labels for improved readability
- ⚡ Live updates with ClickHouse backend

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Altair
- **Backend:** ClickHouse (fast OLAP database)
- **Language:** Python 3
- **Data Processing:** Pandas

---

## 🗂️ Project Structure
''' bash
Realtime_Sales_Analytics/
├── dashboard.py                  # Streamlit dashboard app
├── realtime_sales_analytics.py  # Backend logic with ClickHouse queries
├── requirements.txt             # Python dependencies
├── README.md                    # Project overview & usage guide
├── .gitignore                   # Files/directories to be ignored by Git
└── assets/                      # Asset files (images for previews)
    ├── Dashboard-preview-1.png
    ├── Dashboard-preview-2.png
    └── Dashboard-preview-3.png
