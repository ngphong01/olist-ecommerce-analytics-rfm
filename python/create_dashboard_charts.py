import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
MOCKUP_DIR = os.path.join(BASE_DIR, "powerbi", "dashboard_mockup")
os.makedirs(MOCKUP_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.dpi"] = 300

rfm_path = os.path.join(PROCESSED_DIR, "rfm_customer_segments.csv")
if os.path.exists(rfm_path):
    df_rfm = pd.read_csv(rfm_path)
    seg_summary = df_rfm.groupby("Customer_Segment")["Monetary"].sum().reset_index()
    seg_summary = seg_summary.sort_values(by="Monetary", ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#2b5c8f", "#418ab3", "#e06666", "#f6b26b", "#9fc5e8", "#b6d7a8", "#d5a6bd"]
    bars = ax.barh(seg_summary["Customer_Segment"], seg_summary["Monetary"] / 1e6, color=colors[:len(seg_summary)])
    ax.invert_yaxis()
    ax.set_title("Revenue Contribution by Customer RFM Segment (Million BRL)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Total Revenue (Million BRL)", fontsize=11)
    
    total_rev = seg_summary["Monetary"].sum() / 1e6
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f"{width:.2f}M ({width / total_rev * 100:.1f}%)", 
                va="center", fontsize=10, fontweight="bold", color="#333333")
    
    plt.tight_layout()
    chart1_path = os.path.join(MOCKUP_DIR, "01_rfm_revenue_distribution.png")
    plt.savefig(chart1_path)
    plt.close()

orders_path = os.path.join(RAW_DIR, "orders.csv")
reviews_path = os.path.join(RAW_DIR, "order_reviews.csv")
if os.path.exists(orders_path) and os.path.exists(reviews_path):
    df_o = pd.read_csv(orders_path)
    df_r = pd.read_csv(reviews_path)
    df_o = df_o[df_o["order_status"] == "delivered"].dropna(subset=["order_delivered_customer_date"])
    df_o["purchase"] = pd.to_datetime(df_o["order_purchase_timestamp"])
    df_o["delivered"] = pd.to_datetime(df_o["order_delivered_customer_date"])
    df_o["delivery_days"] = (df_o["delivered"] - df_o["purchase"]).dt.days
    
    merged = df_o.merge(df_r, on="order_id")
    def group_days(d):
        if d <= 5: return "Fast (<= 5 days)"
        elif d <= 12: return "Normal (6 - 12 days)"
        else: return "Late (> 12 days)"
    merged["delivery_group"] = merged["delivery_days"].apply(group_days)
    
    csat = merged.groupby("delivery_group")["review_score"].agg(["mean", "count"]).reset_index()
    order_dict = {"Fast (<= 5 days)": 1, "Normal (6 - 12 days)": 2, "Late (> 12 days)": 3}
    csat["sort"] = csat["delivery_group"].map(order_dict)
    csat = csat.sort_values(by="sort")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bar_colors = ["#2e7d32", "#1976d2", "#d32f2f"]
    bars = ax.bar(csat["delivery_group"], csat["mean"], color=bar_colors, width=0.5)
    ax.set_ylim(0, 5.5)
    ax.set_title("Impact of Delivery Speed on Customer Review Score (CSAT)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Average Review Score (1 - 5 Stars)", fontsize=11)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.15, f"{height:.2f} Stars", 
                ha="center", fontsize=11, fontweight="bold", color="#222222")
                
    plt.tight_layout()
    chart2_path = os.path.join(MOCKUP_DIR, "02_delivery_speed_vs_csat.png")
    plt.savefig(chart2_path)
    plt.close()

items_path = os.path.join(RAW_DIR, "order_items.csv")
if os.path.exists(items_path):
    df_it = pd.read_csv(items_path)
    merged_sales = df_o.merge(df_it, on="order_id")
    merged_sales["year_month"] = merged_sales["purchase"].dt.to_period("M").astype(str)
    monthly = merged_sales.groupby("year_month")["price"].sum().reset_index()
    monthly = monthly.sort_values(by="year_month")
    
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly["year_month"], monthly["price"] / 1e3, marker="o", color="#1a5276", linewidth=2.5, markersize=5)
    ax.fill_between(monthly["year_month"], monthly["price"] / 1e3, color="#aed6f1", alpha=0.35)
    ax.set_title("Monthly Revenue Trend (Thousand BRL)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Revenue (Thousand BRL)", fontsize=11)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    chart3_path = os.path.join(MOCKUP_DIR, "03_monthly_revenue_trend.png")
    plt.savefig(chart3_path)
    plt.close()
