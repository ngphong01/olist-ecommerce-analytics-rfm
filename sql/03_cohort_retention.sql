WITH customer_cohort AS (
    SELECT 
        c.customer_unique_id,
        MIN(DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP))) AS cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),

order_activities AS (
    SELECT DISTINCT
        c.customer_unique_id,
        DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
),

cohort_index_calc AS (
    SELECT 
        cc.customer_unique_id,
        cc.cohort_month,
        oa.order_month,
        (EXTRACT(YEAR FROM oa.order_month) - EXTRACT(YEAR FROM cc.cohort_month)) * 12 +
        (EXTRACT(MONTH FROM oa.order_month) - EXTRACT(MONTH FROM cc.cohort_month)) AS cohort_index
    FROM customer_cohort cc
    JOIN order_activities oa ON cc.customer_unique_id = oa.customer_unique_id
),

cohort_counts AS (
    SELECT 
        cohort_month,
        cohort_index,
        COUNT(DISTINCT customer_unique_id) AS active_customers
    FROM cohort_index_calc
    GROUP BY cohort_month, cohort_index
),

cohort_sizes AS (
    SELECT 
        cohort_month,
        active_customers AS cohort_size
    FROM cohort_counts
    WHERE cohort_index = 0
)

SELECT 
    cc.cohort_month,
    cs.cohort_size,
    cc.cohort_index,
    cc.active_customers,
    ROUND(cc.active_customers * 100.0 / cs.cohort_size, 2) AS retention_rate_pct
FROM cohort_counts cc
JOIN cohort_sizes cs ON cc.cohort_month = cs.cohort_month
ORDER BY cc.cohort_month, cc.cohort_index;
