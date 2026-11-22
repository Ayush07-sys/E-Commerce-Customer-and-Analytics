
{{
    config(
        materialized='view'
    )
}}

SELECT
    customer_id,
    created_at,
    country_code,
    acquisition_channel,
    customer_segment

FROM {{ source('ecommerce', 'customers') }}
