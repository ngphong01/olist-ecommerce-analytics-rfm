WITH reference_date AS (
    SELECT MAX(CAST(order_purchase_timestamp AS TIMESTAMP)) + INTERVAL '1 day' AS max_date
    FROM orders
    WHERE order_status = 'delivered'
),

raw_rfm AS (
    SELECT 
        c.customer_unique_id,
        DATEDIFF('day', MAX(CAST(o.order_purchase_timestamp AS TIMESTAMP)), ref.max_date) AS recency_days,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(oi.price), 0) AS monetary
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    CROSS JOIN reference_date ref
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id, ref.max_date
),

rfm_scores AS (
    SELECT 
        customer_unique_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        CASE 
            WHEN frequency >= 4 THEN 5
            WHEN frequency = 3 THEN 4
            WHEN frequency = 2 THEN 3
            ELSE 1
        END AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM raw_rfm
),

segmented_customers AS (
    SELECT 
        customer_unique_id,
        recency_days,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        CONCAT(r_score, f_score, m_score) AS rfm_code,
        CASE 
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions (Khách VIP)'
            WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers (Trung thành)'
            WHEN r_score >= 4 AND f_score = 1 THEN 'Recent Customers (Khách mới)'
            WHEN r_score >= 3 AND f_score <= 2 AND m_score >= 3 THEN 'Potential Loyalists (Tiềm năng)'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk (Nguy cơ rời bỏ)'
            WHEN r_score = 1 AND f_score >= 4 THEN 'Cant Lose Them (Không thể để mất)'
            WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Hibernating / Lost (Khách ngủ quên/Mất hẳn)'
            ELSE 'Others / Need Attention (Cần quan tâm)'
        END AS customer_segment
    FROM rfm_scores
)

SELECT 
    customer_segment,
    COUNT(customer_unique_id) AS total_customers,
    ROUND(COUNT(customer_unique_id) * 100.0 / SUM(COUNT(customer_unique_id)) OVER(), 2) AS customer_percentage,
    ROUND(SUM(monetary), 0) AS total_revenue,
    ROUND(SUM(monetary) * 100.0 / SUM(SUM(monetary)) OVER(), 2) AS revenue_contribution_pct,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 2) AS avg_orders,
    ROUND(AVG(monetary), 0) AS avg_customer_value
FROM segmented_customers
GROUP BY customer_segment
ORDER BY total_revenue DESC;
