
{{
    config(materialized='view')
}}

SELECT
    payment_id,
    order_id,
    paid_at,
    payment_method,
    payment_status,
    amount

FROM {{ source('ecommerce', 'payments') }}
