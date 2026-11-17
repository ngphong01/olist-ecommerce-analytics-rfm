import os
from datetime import timedelta
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

df_customers = pd.read_csv(os.path.join(RAW_DIR, "customers.csv"))
df_orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))
df_items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))
df_reviews = pd.read_csv(os.path.join(RAW_DIR, "order_reviews.csv"))

df_orders["order_purchase_timestamp"] = pd.to_datetime(df_orders["order_purchase_timestamp"])
df_orders["order_delivered_customer_date"] = pd.to_datetime(df_orders["order_delivered_customer_date"])
df_orders["order_estimated_delivery_date"] = pd.to_datetime(df_orders["order_estimated_delivery_date"])

df_delivered = df_orders[df_orders["order_status"] == "delivered"].copy()

df_merged = df_delivered.merge(df_items, on="order_id", how="inner")
df_merged = df_merged.merge(df_customers, on="customer_id", how="inner")

total_revenue = df_merged["price"].sum()
total_orders = df_delivered["order_id"].nunique()
unique_buyers = df_merged["customer_unique_id"].nunique()
aov = total_revenue / total_orders

print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Delivered Orders: {total_orders:,}")
print(f"Unique Buyers: {unique_buyers:,}")
print(f"AOV: {aov:,.2f}")

snapshot_date = df_merged["order_purchase_timestamp"].max() + timedelta(days=1)

rfm = df_merged.groupby("customer_unique_id").agg({
    "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
    "order_id": "nunique",
    "price": "sum"
}).reset_index()

rfm.columns = ["customer_unique_id", "Recency", "Frequency", "Monetary"]

rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)

def score_freq(x):
    if x >= 4:
        return 5
    elif x == 3:
        return 4
    elif x == 2:
        return 3
    else:
        return 1
rfm["F_Score"] = rfm["Frequency"].apply(score_freq)

rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

def assign_segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3:
        return "Loyal Customers"
    elif r >= 4 and f == 1:
        return "Recent Customers"
    elif r >= 3 and f <= 2 and m >= 3:
        return "Potential Loyalists"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r == 1 and f >= 4:
        return "Cant Lose Them"
    elif r <= 2 and f <= 2 and m <= 2:
        return "Hibernating"
    else:
        return "Need Attention"

rfm["Customer_Segment"] = rfm.apply(assign_segment, axis=1)

summary = rfm.groupby("Customer_Segment").agg(
    Customer_Count=("customer_unique_id", "count"),
    Total_Revenue=("Monetary", "sum"),
    Avg_Revenue=("Monetary", "mean"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean")
).reset_index()

summary["Customer_Pct"] = (summary["Customer_Count"] / summary["Customer_Count"].sum() * 100).round(2)
summary["Revenue_Pct"] = (summary["Total_Revenue"] / summary["Total_Revenue"].sum() * 100).round(2)
summary = summary.sort_values(by="Total_Revenue", ascending=False)

print(summary.to_string(index=False))

output_path = os.path.join(PROCESSED_DIR, "rfm_customer_segments.csv")
rfm.to_csv(output_path, index=False)
