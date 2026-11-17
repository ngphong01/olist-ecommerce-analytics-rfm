SELECT 
    order_status, 
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

DROP VIEW IF EXISTS vw_clean_orders;

CREATE VIEW vw_clean_orders AS
SELECT 
    o.order_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_region,
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS order_date,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS delivered_date,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_date,
    DATEDIFF('day', CAST(o.order_purchase_timestamp AS TIMESTAMP), CAST(o.order_delivered_customer_date AS TIMESTAMP)) AS delivery_duration_days,
    CASE 
        WHEN CAST(o.order_delivered_customer_date AS TIMESTAMP) > CAST(o.order_estimated_delivery_date AS TIMESTAMP) THEN 1 
        ELSE 0 
    END AS is_late_delivery
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL;

SELECT 
    COUNT(DISTINCT order_id) AS orders_in_items,
    ROUND(SUM(price), 0) AS total_gross_merchandise_value,
    ROUND(AVG(price), 0) AS average_item_price
FROM order_items;
