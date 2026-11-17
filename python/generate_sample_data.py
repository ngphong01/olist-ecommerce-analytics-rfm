import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

num_customers = 5000
cities = ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ", "Nha Trang", "Bình Dương", "Đồng Nai"]

customers_data = []
for i in range(1, num_customers + 1):
    city = random.choice(cities)
    state = "Miền Bắc" if city in ["Hà Nội", "Hải Phòng"] else ("Miền Trung" if city in ["Đà Nẵng", "Nha Trang"] else "Miền Nam")
    customers_data.append({
        "customer_id": f"CUST_{i:05d}",
        "customer_unique_id": f"UID_{((i * 17) % 3800) + 1:04d}",
        "customer_city": city,
        "customer_region": state
    })
df_customers = pd.DataFrame(customers_data)
df_customers.to_csv(os.path.join(RAW_DIR, "customers.csv"), index=False)

categories = [
    ("Điện tử & Phụ kiện", 150000, 2500000),
    ("Thời trang nam/nữ", 80000, 750000),
    ("Mỹ phẩm & Làm đẹp", 120000, 1200000),
    ("Nhà cửa & Đời sống", 50000, 950000),
    ("Thực phẩm & Bách hóa", 30000, 350000),
    ("Mẹ & Bé", 90000, 1500000),
]

products_data = []
for i in range(1, 201):
    cat, min_p, max_p = random.choice(categories)
    products_data.append({
        "product_id": f"PROD_{i:04d}",
        "product_category": cat,
        "cost_price": round(random.uniform(min_p, max_p), -3),
    })
df_products = pd.DataFrame(products_data)
df_products.to_csv(os.path.join(RAW_DIR, "products.csv"), index=False)

num_orders = 12000
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 6, 30)
delta_days = (end_date - start_date).days

orders_data = []
order_items_data = []
reviews_data = []

statuses = ["delivered", "delivered", "delivered", "delivered", "shipped", "canceled"]

for order_idx in range(1, num_orders + 1):
    order_id = f"ORD_{order_idx:06d}"
    cust = df_customers.sample(1).iloc[0]
    cust_id = cust["customer_id"]
    
    purchase_day = start_date + timedelta(days=random.randint(0, delta_days), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    status = random.choice(statuses)
    
    est_delivery = purchase_day + timedelta(days=random.randint(3, 5))
    
    actual_delivery = None
    if status == "delivered":
        if random.random() < 0.8:
            actual_delivery = purchase_day + timedelta(days=random.randint(2, 4))
        else:
            actual_delivery = purchase_day + timedelta(days=random.randint(6, 12))
            
    orders_data.append({
        "order_id": order_id,
        "customer_id": cust_id,
        "order_status": status,
        "order_purchase_timestamp": purchase_day.strftime("%Y-%m-%d %H:%M:%S"),
        "order_delivered_customer_date": actual_delivery.strftime("%Y-%m-%d %H:%M:%S") if actual_delivery else "",
        "order_estimated_delivery_date": est_delivery.strftime("%Y-%m-%d %H:%M:%S")
    })
    
    num_items = random.choices([1, 2, 3, 4], weights=[0.65, 0.2, 0.1, 0.05])[0]
    for item_idx in range(1, num_items + 1):
        prod = df_products.sample(1).iloc[0]
        price = round(prod["cost_price"] * random.uniform(1.15, 1.40), -3)
        freight = round(random.choice([15000, 25000, 35000, 50000]), 0)
        
        order_items_data.append({
            "order_id": order_id,
            "order_item_id": item_idx,
            "product_id": prod["product_id"],
            "price": price,
            "freight_value": freight
        })
        
    if status == "delivered" and actual_delivery:
        delivery_days = (actual_delivery - purchase_day).days
        if delivery_days > 5:
            score = random.choices([1, 2, 3, 4, 5], weights=[0.45, 0.25, 0.15, 0.1, 0.05])[0]
        else:
            score = random.choices([1, 2, 3, 4, 5], weights=[0.02, 0.03, 0.10, 0.35, 0.50])[0]
            
        reviews_data.append({
            "review_id": f"REV_{order_idx:06d}",
            "order_id": order_id,
            "review_score": score,
            "review_creation_date": (actual_delivery + timedelta(days=1)).strftime("%Y-%m-%d")
        })

df_orders = pd.DataFrame(orders_data)
df_orders.to_csv(os.path.join(RAW_DIR, "orders.csv"), index=False)

df_order_items = pd.DataFrame(order_items_data)
df_order_items.to_csv(os.path.join(RAW_DIR, "order_items.csv"), index=False)

df_reviews = pd.DataFrame(reviews_data)
df_reviews.to_csv(os.path.join(RAW_DIR, "order_reviews.csv"), index=False)
