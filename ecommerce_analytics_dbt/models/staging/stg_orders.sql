
{{
    config(
        materialized='view'
    )
}}

SELECT
    order_id,
    customer_id,
    ordered_at,
    order_status,
    currency,
    subtotal,
    tax_amount,
    shipping_amount,
    order_total

FROM {{ source('ecommerce', 'orders') }}
