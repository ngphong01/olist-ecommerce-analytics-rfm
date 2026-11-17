import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_OLIST_DIR = os.path.join(BASE_DIR, "data", "raw", "olist")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

print("Processing Olist Customers...")
df_customers = pd.read_csv(os.path.join(RAW_OLIST_DIR, "olist_customers_dataset.csv"))
df_customers = df_customers[["customer_id", "customer_unique_id", "customer_city", "customer_state"]].copy()
df_customers.rename(columns={"customer_state": "customer_region"}, inplace=True)
df_customers.to_csv(os.path.join(RAW_DIR, "customers.csv"), index=False)
print(f"Saved customers.csv: {len(df_customers):,} rows")

print("Processing Olist Products...")
df_products = pd.read_csv(os.path.join(RAW_OLIST_DIR, "olist_products_dataset.csv"))
df_trans = pd.read_csv(os.path.join(RAW_OLIST_DIR, "product_category_name_translation.csv"))
df_products = df_products.merge(df_trans, on="product_category_name", how="left")
df_products["product_category"] = df_products["product_category_name_english"].fillna("others")
df_products["cost_price"] = 0
df_products = df_products[["product_id", "product_category", "cost_price"]].copy()
df_products.to_csv(os.path.join(RAW_DIR, "products.csv"), index=False)
print(f"Saved products.csv: {len(df_products):,} rows")

print("Processing Olist Orders...")
df_orders = pd.read_csv(os.path.join(RAW_OLIST_DIR, "olist_orders_dataset.csv"))
df_orders = df_orders[[
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]].copy()
df_orders.to_csv(os.path.join(RAW_DIR, "orders.csv"), index=False)
print(f"Saved orders.csv: {len(df_orders):,} rows")

print("Processing Olist Order Items...")
df_items = pd.read_csv(os.path.join(RAW_OLIST_DIR, "olist_order_items_dataset.csv"))
df_items = df_items[["order_id", "order_item_id", "product_id", "price", "freight_value"]].copy()
df_items.to_csv(os.path.join(RAW_DIR, "order_items.csv"), index=False)
print(f"Saved order_items.csv: {len(df_items):,} rows")

print("Processing Olist Reviews...")
df_reviews = pd.read_csv(os.path.join(RAW_OLIST_DIR, "olist_order_reviews_dataset.csv"))
df_reviews = df_reviews[["review_id", "order_id", "review_score", "review_creation_date"]].copy()
df_reviews.drop_duplicates(subset=["review_id"], inplace=True)
df_reviews.to_csv(os.path.join(RAW_DIR, "order_reviews.csv"), index=False)
print(f"Saved order_reviews.csv: {len(df_reviews):,} rows")

print("Transformation completed successfully.")
