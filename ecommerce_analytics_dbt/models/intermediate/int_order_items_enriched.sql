
{{
    config(
        materialized='view'
    )
}}

SELECT
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.discount_amount,
    oi.line_total,

    p.product_name,
    p.category,
    p.unit_cost,

    o.customer_id,
    o.ordered_at,
    o.order_status,

    -- Revenue, cost and profitability
    oi.line_total AS product_revenue,
    oi.quantity * p.unit_cost AS product_cost,

    oi.line_total - (oi.quantity * p.unit_cost) AS gross_profit,

    CASE
        WHEN oi.line_total > 0
        THEN ROUND(
            (
                (oi.line_total - (oi.quantity * p.unit_cost))
                / oi.line_total
            ) * 100, 2
        )
        ELSE 0
    END AS profit_margin_percentage

FROM {{ ref('stg_order_items') }} oi

LEFT JOIN {{ ref('stg_products') }} p
    ON oi.product_id = p.product_id

LEFT JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id
