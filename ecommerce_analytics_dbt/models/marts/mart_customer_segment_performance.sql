
{{
    config(
        materialized='view'
    )
}}

SELECT
    customer_segment,

    -- Customer metrics
    COUNT(customer_id) AS total_customers,

    COUNT(*) FILTER (
        WHERE total_orders > 0
    ) AS purchasing_customers,

    COUNT(*) FILTER (
        WHERE total_orders > 1
    ) AS repeat_customers,

    -- Purchase metrics
    SUM(total_orders) AS total_orders,

    SUM(total_spending) AS total_revenue,

    ROUND(
        AVG(total_spending),
        2
    ) AS average_customer_spending,

    ROUND(
        AVG(average_order_value) FILTER (
            WHERE total_orders > 0
        ),
        2
    ) AS average_order_value,

    -- Customer repeat rate
    ROUND(
        COUNT(*) FILTER (
            WHERE total_orders > 1
        )::NUMERIC
        / NULLIF(
            COUNT(*) FILTER (
                WHERE total_orders > 0
            ),
            0
        ) * 100,
        2
    ) AS repeat_customer_rate

FROM {{ ref('dim_customers') }}

GROUP BY customer_segment
