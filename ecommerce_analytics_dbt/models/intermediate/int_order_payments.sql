WITH payment_summary AS (
    SELECT
        order_id,
        SUM(amount) AS successful_payment
    FROM {{ ref('stg_payments') }}
    WHERE payment_status = 'succeeded'
    GROUP BY order_id
),

refund_summary AS (
    SELECT
        order_id,
        SUM(amount) AS refund_amount
    FROM {{ ref('stg_refunds') }}
    GROUP BY order_id
)

SELECT
    COALESCE(p.order_id, r.order_id) AS order_id,
    COALESCE(p.successful_payment, 0) AS successful_payment,
    COALESCE(r.refund_amount, 0) AS refund_amount,
    COALESCE(p.successful_payment, 0)
        - COALESCE(r.refund_amount, 0) AS net_collected

FROM payment_summary p

FULL OUTER JOIN refund_summary r
    ON p.order_id = r.order_id