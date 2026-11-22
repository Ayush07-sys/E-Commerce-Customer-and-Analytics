
{{
    config(
        materialized='view'
    )
}}

SELECT
    -- Customer profile
    c.customer_id,
    c.country_code,
    c.acquisition_channel,
    c.customer_segment,
    c.created_at,

    -- Purchase metrics
    COALESCE(o.total_orders, 0) AS total_orders,
    COALESCE(o.total_spending, 0) AS total_spending,
    COALESCE(o.average_order_value, 0) AS average_order_value,

    -- Purchase dates
    o.first_purchase_date,
    o.last_purchase_date,

    -- Customer recency
    o.days_since_last_purchase

FROM {{ ref('stg_customers') }} c

LEFT JOIN {{ ref('int_customer_orders') }} o
    ON c.customer_id = o.customer_id
