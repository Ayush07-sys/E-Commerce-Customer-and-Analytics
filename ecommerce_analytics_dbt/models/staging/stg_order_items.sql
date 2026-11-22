
{{
    config(materialized='view')
}}

SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_amount,
    line_total

FROM {{ source('ecommerce', 'order_items') }}
