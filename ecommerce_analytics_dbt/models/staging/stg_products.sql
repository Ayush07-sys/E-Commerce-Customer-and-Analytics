
{{
    config(materialized='view')
}}

SELECT
    product_id,
    sku,
    product_name,
    category,
    unit_cost,
    list_price

FROM {{ source('ecommerce', 'products') }}
