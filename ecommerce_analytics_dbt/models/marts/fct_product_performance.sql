
{{
    config(
        materialized='view'
    )
}}

SELECT
    product_id,
    product_name,
    category,

    -- Sales metrics
    SUM(quantity) AS total_units_sold,
    COUNT(DISTINCT order_id) AS total_orders,

    -- Revenue and cost
    SUM(product_revenue) AS total_revenue,
    SUM(product_cost) AS total_cost,

    -- Profitability
    SUM(gross_profit) AS total_gross_profit,

    CASE
        WHEN SUM(product_revenue) > 0
        THEN ROUND(
            SUM(gross_profit) / SUM(product_revenue) * 100,
            2
        )
        ELSE 0
    END AS profit_margin_percentage

FROM {{ ref('int_order_items_enriched') }}

WHERE order_status <> 'cancelled'

GROUP BY
    product_id,
    product_name,
    category
