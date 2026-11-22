
{{
    config(
        materialized='view'
    )
}}

SELECT
    customer_id,

    -- Order metrics
    COUNT(order_id) AS total_orders,

    SUM(order_total) AS total_spending,

    ROUND(
        AVG(order_total),
        2
    ) AS average_order_value,

    -- Purchase dates
    MIN(ordered_at) AS first_purchase_date,

    MAX(ordered_at) AS last_purchase_date,

    -- Customer recency
    CURRENT_DATE - MAX(ordered_at)::DATE AS days_since_last_purchase

FROM {{ ref('stg_orders') }}

WHERE order_status <> 'cancelled'

GROUP BY customer_id
