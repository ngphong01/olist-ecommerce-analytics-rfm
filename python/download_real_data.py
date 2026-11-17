import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_OLIST_DIR = os.path.join(BASE_DIR, "data", "raw", "olist")
os.makedirs(RAW_OLIST_DIR, exist_ok=True)

files = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "product_category_name_translation.csv"
]

base_url = "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/"

for f in files:
    url = base_url + f
    dest = os.path.join(RAW_OLIST_DIR, f)
    print(f"Downloading {f}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as out:
        out.write(resp.read())
    print(f"Done: {dest} ({os.path.getsize(dest):,} bytes)")

print("All real data files downloaded successfully.")
