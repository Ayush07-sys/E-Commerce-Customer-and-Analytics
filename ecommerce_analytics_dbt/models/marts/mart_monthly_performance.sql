
{{
    config(
        materialized='view'
    )
}}

WITH monthly_orders AS (

    SELECT
        DATE_TRUNC('month', ordered_at) AS order_month,
        COUNT(order_id) AS total_orders,
        SUM(order_total) AS total_order_revenue

    FROM {{ ref('stg_orders') }}

    WHERE order_status <> 'cancelled'

    GROUP BY DATE_TRUNC('month', ordered_at)

),

monthly_products AS (

    SELECT
        DATE_TRUNC('month', ordered_at) AS order_month,

        SUM(product_revenue) AS total_product_revenue,
        SUM(product_cost) AS total_product_cost,
        SUM(gross_profit) AS total_gross_profit

    FROM {{ ref('int_order_items_enriched') }}

    WHERE order_status <> 'cancelled'

    GROUP BY DATE_TRUNC('month', ordered_at)

)

SELECT
    o.order_month,

    -- Order metrics
    o.total_orders,
    o.total_order_revenue,

    -- Product metrics
    p.total_product_revenue,
    p.total_product_cost,
    p.total_gross_profit,

    -- Product profit margin
    CASE
        WHEN p.total_product_revenue > 0
        THEN ROUND(
            p.total_gross_profit
            / p.total_product_revenue * 100,
            2
        )
        ELSE 0
    END AS profit_margin_percentage

FROM monthly_orders o

LEFT JOIN monthly_products p
    ON o.order_month = p.order_month
