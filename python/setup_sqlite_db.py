import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "ecommerce.db")

conn = sqlite3.connect(DB_PATH)

files = [
    ("customers.csv", "customers"),
    ("products.csv", "products"),
    ("orders.csv", "orders"),
    ("order_items.csv", "order_items"),
    ("order_reviews.csv", "order_reviews")
]

for csv_file, table_name in files:
    file_path = os.path.join(RAW_DIR, csv_file)
    if os.path.exists(file_path):
        print(f"Loading {table_name} into SQLite...")
        for chunk in pd.read_csv(file_path, chunksize=25000):
            chunk.to_sql(table_name, conn, if_exists="append" if chunk.index[0] > 0 else "replace", index=False)

cursor = conn.cursor()
cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_order ON order_items(order_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_product ON order_items(product_id);")
conn.commit()
conn.close()
print("SQLite database populated successfully.")
