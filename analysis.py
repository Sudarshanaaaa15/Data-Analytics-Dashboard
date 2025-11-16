from pymongo import MongoClient
from datetime import datetime
import pandas as pd

# -----------------------------
# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://sudarshan:Suda8867@resumejdanalyzer.key36hn.mongodb.net/?appName=ResumeJDAnalyzer")
db = client['amazon_data']
collection = db['sales_report']

# -----------------------------
# Convert 'Date' strings to datetime
for doc in collection.find({"Date": {"$type": "string"}}, {"_id": 1, "Date": 1}):
    try:
        date_obj = datetime.strptime(doc['Date'], '%m-%d-%y')  # Adjust format if needed
        collection.update_one({"_id": doc["_id"]}, {"$set": {"Date": date_obj}})
    except:
        continue

# -----------------------------
# Load full data into pandas
docs = list(collection.find({}))
df = pd.DataFrame(docs)

# Ensure numeric Amount
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0)
df['B2B'] = df['B2B'].fillna(0).astype(int)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# -----------------------------
# 1. Total Revenue & Orders
def get_total_sales():
    total_revenue = df['Amount'].sum()
    total_orders = len(df)
    avg_order_value = df['Amount'].mean()
    return total_revenue, total_orders, avg_order_value

# -----------------------------
# 2. Monthly Sales Trend
def get_monthly_sales():
    monthly = df.groupby([df['Date'].dt.to_period('M')])['Amount'].sum().reset_index()
    monthly['Date'] = monthly['Date'].dt.to_timestamp()
    return monthly

# -----------------------------
# 3. Top-Selling Categories
def get_top_categories(top_n=10):
    by_qty = df.groupby('Category')['Qty'].sum().sort_values(ascending=False).head(top_n).reset_index()
    by_revenue = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(top_n).reset_index()
    return by_qty, by_revenue

# -----------------------------
# 4. Customer Segmentation
def get_customer_segmentation():
    seg = df.groupby('B2B').agg(TotalOrders=('Amount','count'), TotalRevenue=('Amount','sum')).reset_index()
    seg['Label'] = seg['B2B'].apply(lambda x: 'B2B' if x==1 else 'Individual')
    return seg

# -----------------------------
# 5. Geographical Analysis
def get_top_states(top_n=10):
    state_df = df.groupby('ship-state')['Amount'].sum().sort_values(ascending=False).head(top_n).reset_index()
    return state_df

def get_top_cities(top_n=10):
    city_df = df.groupby('ship-city')['Amount'].sum().sort_values(ascending=False).head(top_n).reset_index()
    return city_df

# -----------------------------
# High-Value Orders (>5000)
def get_high_value_orders(threshold=5000):
    high_value = df.groupby('Order ID')['Amount'].sum().reset_index()
    return high_value[high_value['Amount'] > threshold]