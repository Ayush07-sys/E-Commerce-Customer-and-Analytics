
{{
    config(materialized='view')
}}

SELECT
    refund_id,
    payment_id,
    order_id,
    refunded_at,
    refund_reason,
    amount

FROM {{ source('ecommerce', 'refunds') }}
