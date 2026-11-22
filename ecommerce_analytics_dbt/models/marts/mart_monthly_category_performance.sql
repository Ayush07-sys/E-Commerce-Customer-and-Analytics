
{{
    config(
        materialized='view'
    )
}}

SELECT
    DATE_TRUNC('month', ordered_at)::date AS order_month,
    category,

    -- Revenue, cost and profit
    SUM(product_revenue) AS total_product_revenue,
    SUM(product_cost) AS total_product_cost,
    SUM(gross_profit) AS total_gross_profit,

    -- Profit margin percentage
    CASE
        WHEN SUM(product_revenue) > 0
        THEN ROUND(
            (
                SUM(gross_profit) /
                SUM(product_revenue)
            ) * 100,
            2
        )
        ELSE 0
    END AS profit_margin_percentage

FROM {{ ref('int_order_items_enriched') }}

WHERE LOWER(order_status) <> 'cancelled'

GROUP BY
    DATE_TRUNC('month', ordered_at)::date,
    category
