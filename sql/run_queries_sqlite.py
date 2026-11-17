import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "ecommerce.db")

conn = sqlite3.connect(DB_PATH)

q1 = """
SELECT 
    order_status, 
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;
"""
df_status = pd.read_sql_query(q1, conn)
print("=== ORDER STATUS ===")
print(df_status.to_string(index=False))

q2 = """
SELECT 
    c.customer_region AS state,
    COUNT(DISTINCT o.order_id) AS total_delivered_orders,
    ROUND(SUM(oi.price), 2) AS total_revenue_brl,
    ROUND(AVG(oi.price), 2) AS avg_item_price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_region
ORDER BY total_revenue_brl DESC
LIMIT 5;
"""
df_region = pd.read_sql_query(q2, conn)
print("\n=== TOP 5 STATES BY REVENUE ===")
print(df_region.to_string(index=False))

q3 = """
SELECT 
    CASE 
        WHEN CAST(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) AS INT) <= 5 THEN 'Fast (<= 5 days)'
        WHEN CAST(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) AS INT) <= 12 THEN 'Normal (6 - 12 days)'
        ELSE 'Late (> 12 days)'
    END AS delivery_group,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(SUM(CASE WHEN r.review_score = 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_5_star,
    ROUND(SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_bad_reviews
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
GROUP BY delivery_group
ORDER BY avg_review_score DESC;
"""
df_review = pd.read_sql_query(q3, conn)
print("\n=== DELIVERY SPEED VS CSAT ===")
print(df_review.to_string(index=False))

conn.close()
