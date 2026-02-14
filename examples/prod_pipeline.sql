WITH monthly_sales AS (
    SELECT
        customer_id,
        TO_CHAR(date, 'YYYY-MM') AS month,
        SUM(amount) AS total_spent,
        COUNT(*) AS purchases
    FROM raw_sales_data
    WHERE (status = 'completed' OR status = 'refunded')
        AND date >= '2023-01-01'
    GROUP BY customer_id, TO_CHAR(date, 'YYYY-MM')
),
customer_metrics AS (
    SELECT
        customer_id,
        month,
        total_spent,
        purchases,
        LAG(total_spent, 1, 0) OVER (PARTITION BY customer_id ORDER BY month) AS previous_month_spend,
        CASE 
            WHEN LAG(total_spent, 1, 0) OVER (PARTITION BY customer_id ORDER BY month) > 0 
                 AND total_spent = 0 
            THEN TRUE 
            ELSE FALSE 
        END AS is_churn_risk,
        SUM(total_spent) OVER (PARTITION BY customer_id ORDER BY month) AS customer_lifetime_value
    FROM monthly_sales
)
SELECT
    customer_id,
    month,
    total_spent,
    purchases,
    previous_month_spend,
    is_churn_risk,
    customer_lifetime_value
FROM customer_metrics
ORDER BY total_spent DESC, customer_id, month;