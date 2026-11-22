select current_database();
create SCHEMA staging;

select schema_name
from information_schema.schemata
where schema_name = 'staging';


CREATE TABLE staging.customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    created_at TIMESTAMP,
    country_code VARCHAR(2),
    acquisition_channel TEXT,
    customer_segment TEXT
);

select count(*)
from staging.customers;


select *
from staging.customers
limit 10;


select customer_id, country_code, acquisition_channel from staging.customers limit 10;


CREATE TABLE staging.orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    ordered_at TIMESTAMPTZ,
    order_status TEXT,
    currency VARCHAR(3),
    subtotal NUMERIC(12,2),
    tax_amount NUMERIC(12,2),
    shipping_amount NUMERIC(12,2),
    order_total NUMERIC(12,2)
);

CREATE TABLE staging.order_items (
    order_item_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20),
    product_id VARCHAR(20),
    quantity INTEGER,
    unit_price NUMERIC(12,2),
    discount_amount NUMERIC(12,2),
    line_total NUMERIC(12,2)
);


CREATE TABLE staging.products (
    product_id VARCHAR(20) PRIMARY KEY,
    sku VARCHAR(50),
    product_name TEXT,
    category TEXT,
    unit_cost NUMERIC(12,2),
    list_price NUMERIC(12,2)
);

CREATE TABLE staging.payments (
    payment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20),
    paid_at TIMESTAMPTZ,
    payment_method TEXT,
    payment_status TEXT,
    amount NUMERIC(12,2)
);


CREATE TABLE staging.refunds (
    refund_id VARCHAR(20) PRIMARY KEY,
    payment_id VARCHAR(20),
    order_id VARCHAR(20),
    refunded_at TIMESTAMPTZ,
    refund_reason TEXT,
    amount NUMERIC(12,2)
);

select * from staging.orders

SELECT 'customers' AS table_name, COUNT(*) FROM staging.customers
UNION ALL
SELECT 'orders', COUNT(*) FROM staging.orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM staging.order_items
UNION ALL
SELECT 'products', COUNT(*) FROM staging.products
UNION ALL
SELECT 'payments', COUNT(*) FROM staging.payments
UNION ALL
SELECT 'refunds', COUNT(*) FROM staging.refunds;

SELECT
    DATE_TRUNC('month', o.ordered_at AT TIME ZONE 'UTC') AS order_month,

    SUM(oi.line_total) AS total_revenue,

    SUM(p.unit_cost * oi.quantity) AS total_cost,

    SUM(oi.line_total)
        - SUM(p.unit_cost * oi.quantity) AS gross_profit,

    ROUND(
        (
            SUM(oi.line_total)
            - SUM(p.unit_cost * oi.quantity)
        ) / NULLIF(SUM(oi.line_total), 0) * 100,
        2
    ) AS gross_margin_pct

FROM staging.orders o

JOIN staging.order_items oi
    ON o.order_id = oi.order_id

JOIN staging.products p
    ON oi.product_id = p.product_id

WHERE o.order_status != 'cancelled'

GROUP BY DATE_TRUNC('month', o.ordered_at AT TIME ZONE 'UTC')

ORDER BY order_month;

SELECT
    MIN(ordered_at) AS first_order,
    MAX(ordered_at) AS last_order,
    COUNT(*) AS total_orders
FROM staging.orders;

WITH payment_summary AS (
    SELECT
        COUNT(*) FILTER (
            WHERE payment_status = 'succeeded'
        ) AS successful_payments,

        COUNT(*) FILTER (
            WHERE payment_status = 'failed'
        ) AS failed_payments,

        SUM(amount) FILTER (
            WHERE payment_status = 'succeeded'
        ) AS successful_amount

    FROM staging.payments
),

refund_summary AS (
    SELECT
        COUNT(*) AS total_refunds,
        SUM(amount) AS total_refund_amount
    FROM staging.refunds
)

SELECT
    p.successful_payments,
    p.failed_payments,
    p.successful_amount,
    r.total_refunds,
    r.total_refund_amount,
    p.successful_amount - r.total_refund_amount
        AS net_collected_amount

FROM payment_summary p
CROSS JOIN refund_summary r;


SELECT
    p.category,
    SUM(oi.line_total) AS total_revenue,
    SUM(p.unit_cost * oi.quantity) AS total_cost,

    SUM(oi.line_total)
        - SUM(p.unit_cost * oi.quantity) AS gross_profit,

    ROUND(
        (
            SUM(oi.line_total)
            - SUM(p.unit_cost * oi.quantity)
        ) / NULLIF(SUM(oi.line_total), 0) * 100,
        2
    ) AS gross_margin_pct

FROM staging.orders o

JOIN staging.order_items oi
    ON o.order_id = oi.order_id

JOIN staging.products p
    ON oi.product_id = p.product_id

WHERE o.order_status != 'cancelled'

GROUP BY p.category
ORDER BY gross_profit DESC;

WITH customer_order_counts AS (
    SELECT
        customer_id,
        COUNT(*) AS order_count
    FROM staging.orders
    WHERE order_status != 'cancelled'
    GROUP BY customer_id
)

SELECT
    COUNT(*) AS purchasing_customers,

    COUNT(*) FILTER (
        WHERE order_count = 1
    ) AS one_time_customers,

    COUNT(*) FILTER (
        WHERE order_count > 1
    ) AS repeat_customers,

    ROUND(
        COUNT(*) FILTER (
            WHERE order_count > 1
        ) * 100.0 / COUNT(*),
        2
    ) AS repeat_purchase_rate_pct

FROM customer_order_counts;


WITH payment_summary AS (
    SELECT
        order_id,
        SUM(amount) FILTER (
            WHERE payment_status = 'succeeded'
        ) AS successful_amount
    FROM staging.payments
    GROUP BY order_id
),

refund_summary AS (
    SELECT
        order_id,
        SUM(amount) AS refund_amount
    FROM staging.refunds
    GROUP BY order_id
),

order_values AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.ordered_at,
        COALESCE(p.successful_amount, 0)
        - COALESCE(r.refund_amount, 0) AS net_amount
    FROM staging.orders o
    LEFT JOIN payment_summary p
        ON o.order_id = p.order_id
    LEFT JOIN refund_summary r
        ON o.order_id = r.order_id
    WHERE o.order_status != 'cancelled'
),

customer_rfm AS (
    SELECT
        customer_id,
        MAX(ordered_at) AS last_purchase,
        COUNT(*) AS frequency,
        SUM(net_amount) AS monetary
    FROM order_values
    GROUP BY customer_id
),

snapshot AS (
    SELECT
        MAX(ordered_at) + INTERVAL '1 day' AS snapshot_date
    FROM order_values
)

SELECT
    c.customer_id,
    (s.snapshot_date::date - c.last_purchase::date) AS recency,
    c.frequency,
    ROUND(c.monetary, 2) AS monetary
FROM customer_rfm c
CROSS JOIN snapshot s
ORDER BY c.customer_id
LIMIT 10;

WITH payment_summary AS (
    SELECT
        order_id,
        SUM(amount) FILTER (
            WHERE payment_status = 'succeeded'
        ) AS successful_amount
    FROM staging.payments
    GROUP BY order_id
),

refund_summary AS (
    SELECT
        order_id,
        SUM(amount) AS refund_amount
    FROM staging.refunds
    GROUP BY order_id
),

order_values AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.ordered_at,
        COALESCE(p.successful_amount, 0)
        - COALESCE(r.refund_amount, 0) AS net_amount
    FROM staging.orders o
    LEFT JOIN payment_summary p USING (order_id)
    LEFT JOIN refund_summary r USING (order_id)
    WHERE o.order_status != 'cancelled'
),

customer_rfm AS (
    SELECT
        customer_id,
        MAX(ordered_at) AS last_purchase,
        COUNT(*) AS frequency,
        SUM(net_amount) AS monetary
    FROM order_values
    GROUP BY customer_id
),

snapshot AS (
    SELECT
        MAX(ordered_at) + INTERVAL '1 day' AS snapshot_date
    FROM order_values
),

rfm_scores AS (
    SELECT
        c.customer_id,
        (s.snapshot_date::date - c.last_purchase::date) AS recency,
        c.frequency,
        c.monetary,

        NTILE(4) OVER (
            ORDER BY c.last_purchase ASC
        ) AS r_score,

        NTILE(4) OVER (
            ORDER BY c.frequency ASC
        ) AS f_score,

        NTILE(4) OVER (
            ORDER BY c.monetary ASC
        ) AS m_score

    FROM customer_rfm c
    CROSS JOIN snapshot s
),

segmented_customers AS (
    SELECT
        *,
        CASE
            WHEN r_score >= 3
             AND f_score >= 3
             AND m_score >= 3
                THEN 'Champions'

            WHEN r_score >= 2
             AND f_score >= 3
                THEN 'Loyal Customers'

            WHEN r_score >= 3
             AND f_score >= 2
                THEN 'Potential Loyalists'

            WHEN r_score = 4
             AND f_score = 1
                THEN 'New Customers'

            WHEN r_score <= 2
             AND f_score >= 3
                THEN 'At Risk'

            ELSE 'Hibernating'
        END AS customer_segment

    FROM rfm_scores
)

SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage
FROM segmented_customers
GROUP BY customer_segment
ORDER BY customer_count DESC;



WITH valid_orders AS (
    SELECT DISTINCT
        customer_id,
        DATE_TRUNC('month', ordered_at AT TIME ZONE 'UTC') AS purchase_month
    FROM staging.orders
    WHERE order_status <> 'cancelled'
),

customer_cohorts AS (
    SELECT
        customer_id,
        MIN(purchase_month) AS cohort_month
    FROM valid_orders
    GROUP BY customer_id
),

cohort_activity AS (
    SELECT
        v.customer_id,
        c.cohort_month,
        v.purchase_month,

        (
            EXTRACT(YEAR FROM v.purchase_month)::INT
            - EXTRACT(YEAR FROM c.cohort_month)::INT
        ) * 12
        +
        EXTRACT(MONTH FROM v.purchase_month)::INT
        - EXTRACT(MONTH FROM c.cohort_month)::INT
        + 1 AS cohort_index

    FROM valid_orders v
    JOIN customer_cohorts c
        ON v.customer_id = c.customer_id
),

cohort_counts AS (
    SELECT
        cohort_month,
        cohort_index,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM cohort_activity
    GROUP BY cohort_month, cohort_index
),

cohort_sizes AS (
    SELECT
        cohort_month,
        active_customers AS cohort_size
    FROM cohort_counts
    WHERE cohort_index = 1
)

SELECT
    cc.cohort_month::DATE AS cohort_month,
    cc.cohort_index,
    cs.cohort_size,
    cc.active_customers,

    ROUND(
        cc.active_customers * 100.0
        / NULLIF(cs.cohort_size, 0),
        2
    ) AS retention_pct

FROM cohort_counts cc
JOIN cohort_sizes cs
    ON cc.cohort_month = cs.cohort_month

ORDER BY
    cc.cohort_month,
    cc.cohort_index;


WITH payment_summary AS (
    SELECT
        order_id,
        SUM(amount) AS successful_payment
    FROM staging.payments
    WHERE payment_status = 'succeeded'
    GROUP BY order_id
),

refund_summary AS (
    SELECT
        order_id,
        SUM(amount) AS refund_amount
    FROM staging.refunds
    GROUP BY order_id
),

customer_spending AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS total_orders,

        SUM(
            COALESCE(p.successful_payment, 0)
            - COALESCE(r.refund_amount, 0)
        ) AS historical_clv

    FROM staging.orders o

    LEFT JOIN payment_summary p
        ON o.order_id = p.order_id

    LEFT JOIN refund_summary r
        ON o.order_id = r.order_id

    WHERE o.order_status <> 'cancelled'

    GROUP BY o.customer_id
),

rfm_segments AS (
    SELECT
        customer_id,
        CASE
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3
                THEN 'Champions'
            WHEN r_score >= 2 AND f_score >= 3
                THEN 'Loyal Customers'
            WHEN r_score >= 3 AND f_score >= 2
                THEN 'Potential Loyalists'
            WHEN r_score = 4 AND f_score = 1
                THEN 'New Customers'
            WHEN r_score <= 2 AND f_score >= 3
                THEN 'At Risk'
            ELSE 'Hibernating'
        END AS customer_segment
    FROM (
        SELECT
            customer_id,
            NTILE(4) OVER (ORDER BY last_purchase ASC) AS r_score,
            NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
            NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
        FROM (
            SELECT
                o.customer_id,
                MAX(o.ordered_at) AS last_purchase,
                COUNT(*) AS frequency,
                SUM(
                    COALESCE(p.successful_payment, 0)
                    - COALESCE(r.refund_amount, 0)
                ) AS monetary
            FROM staging.orders o
            LEFT JOIN payment_summary p
                ON o.order_id = p.order_id
            LEFT JOIN refund_summary r
                ON o.order_id = r.order_id
            WHERE o.order_status <> 'cancelled'
            GROUP BY o.customer_id
        ) customer_rfm
    ) scored
)

SELECT
    r.customer_segment,
    COUNT(*) AS total_customers,
    ROUND(AVG(s.historical_clv), 2) AS average_historical_clv,
    ROUND(SUM(s.historical_clv), 2) AS total_segment_value
FROM customer_spending s
JOIN rfm_segments r
    ON s.customer_id = r.customer_id
GROUP BY r.customer_segment
ORDER BY total_segment_value DESC;


WITH customer_spending AS (
    SELECT
        o.customer_id,
        SUM(o.order_total) AS total_spending
    FROM staging.orders o
    WHERE o.order_status <> 'cancelled'
    GROUP BY o.customer_id
),

rfm AS (
    SELECT
        customer_id,
        NTILE(4) OVER (ORDER BY last_purchase ASC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM (
        SELECT
            customer_id,
            MAX(ordered_at) AS last_purchase,
            COUNT(*) AS frequency,
            SUM(order_total) AS monetary
        FROM staging.orders
        WHERE order_status <> 'cancelled'
        GROUP BY customer_id
    ) x
),

segments AS (
    SELECT
        customer_id,
        CASE
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3
                THEN 'Champions'
            WHEN r_score >= 2 AND f_score >= 3
                THEN 'Loyal Customers'
            WHEN r_score >= 3 AND f_score >= 2
                THEN 'Potential Loyalists'
            WHEN r_score = 4 AND f_score = 1
                THEN 'New Customers'
            WHEN r_score <= 2 AND f_score >= 3
                THEN 'At Risk'
            ELSE 'Hibernating'
        END AS customer_segment
    FROM rfm
),

segment_revenue AS (
    SELECT
        s.customer_segment,
        SUM(c.total_spending) AS segment_revenue
    FROM customer_spending c
    JOIN segments s
        ON c.customer_id = s.customer_id
    GROUP BY s.customer_segment
)

SELECT
    customer_segment,
    ROUND(segment_revenue, 2) AS segment_revenue,
    ROUND(
        segment_revenue * 100.0 /
        SUM(segment_revenue) OVER (),
        2
    ) AS revenue_share_pct
FROM segment_revenue
ORDER BY segment_revenue DESC;





SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.line_total), 2) AS total_revenue,
    ROUND(
        SUM(oi.line_total - p.unit_cost * oi.quantity),
        2
    ) AS gross_profit

FROM staging.orders o

JOIN staging.order_items oi
    ON o.order_id = oi.order_id

JOIN staging.products p
    ON oi.product_id = p.product_id

WHERE o.order_status <> 'cancelled'

GROUP BY
    p.product_id,
    p.product_name,
    p.category

ORDER BY total_revenue DESC
LIMIT 10;



WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC(
            'month',
            o.ordered_at AT TIME ZONE 'UTC'
        ) AS order_month,
        SUM(o.order_total) AS revenue
    FROM staging.orders o
    WHERE o.order_status <> 'cancelled'
    GROUP BY 1
),

growth AS (
    SELECT
        order_month,
        revenue,

        LAG(revenue, 1) OVER (
            ORDER BY order_month
        ) AS previous_month_revenue,

        LAG(revenue, 12) OVER (
            ORDER BY order_month
        ) AS previous_year_revenue

    FROM monthly_revenue
)

SELECT
    order_month::DATE AS order_month,
    ROUND(revenue, 2) AS revenue,

    ROUND(
        (revenue - previous_month_revenue)
        * 100.0 / NULLIF(previous_month_revenue, 0),
        2
    ) AS mom_growth_pct,

    ROUND(
        (revenue - previous_year_revenue)
        * 100.0 / NULLIF(previous_year_revenue, 0),
        2
    ) AS yoy_growth_pct

FROM growth
ORDER BY order_month;


SELECT
    'orders_without_customer' AS validation,
    COUNT(*) AS problem_count
FROM staging.orders o
LEFT JOIN staging.customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL

UNION ALL

SELECT
    'order_items_without_order',
    COUNT(*)
FROM staging.order_items oi
LEFT JOIN staging.orders o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL

UNION ALL

SELECT
    'order_items_without_product',
    COUNT(*)
FROM staging.order_items oi
LEFT JOIN staging.products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL

UNION ALL

SELECT
    'payments_without_order',
    COUNT(*)
FROM staging.payments p
LEFT JOIN staging.orders o
    ON p.order_id = o.order_id
WHERE o.order_id IS NULL

UNION ALL

SELECT
    'refunds_without_order',
    COUNT(*)
FROM staging.refunds r
LEFT JOIN staging.orders o
    ON r.order_id = o.order_id
WHERE o.order_id IS NULL

ORDER BY validation;



SELECT
    'customers' AS table_name,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_ids
FROM staging.customers

UNION ALL

SELECT
    'orders',
    COUNT(*),
    COUNT(DISTINCT order_id)
FROM staging.orders

UNION ALL

SELECT
    'order_items',
    COUNT(*),
    COUNT(DISTINCT order_item_id)
FROM staging.order_items

UNION ALL

SELECT
    'products',
    COUNT(*),
    COUNT(DISTINCT product_id)
FROM staging.products

UNION ALL

SELECT
    'payments',
    COUNT(*),
    COUNT(DISTINCT payment_id)
FROM staging.payments

UNION ALL

SELECT
    'refunds',
    COUNT(*),
    COUNT(DISTINCT refund_id)
FROM staging.refunds

ORDER BY table_name;




CREATE SCHEMA IF NOT EXISTS analytics;




CREATE OR REPLACE VIEW analytics.monthly_performance AS

SELECT
    DATE_TRUNC(
        'month',
        o.ordered_at AT TIME ZONE 'UTC'
    )::DATE AS order_month,

    SUM(oi.line_total) AS total_revenue,

    SUM(p.unit_cost * oi.quantity) AS total_cost,

    SUM(oi.line_total)
        - SUM(p.unit_cost * oi.quantity) AS gross_profit,

    ROUND(
        (
            SUM(oi.line_total)
            - SUM(p.unit_cost * oi.quantity)
        ) * 100.0
        / NULLIF(SUM(oi.line_total), 0),
        2
    ) AS gross_margin_pct

FROM staging.orders o

JOIN staging.order_items oi
    ON o.order_id = oi.order_id

JOIN staging.products p
    ON oi.product_id = p.product_id

WHERE o.order_status <> 'cancelled'

GROUP BY 1;



SELECT *
FROM analytics.monthly_performance
ORDER BY order_month;



CREATE OR REPLACE VIEW analytics.customer_analytics AS


WITH payment_summary AS (
    SELECT
        order_id,
        SUM(amount) AS successful_payment
    FROM staging.payments
    WHERE payment_status = 'succeeded'
    GROUP BY order_id
),

refund_summary AS (
    SELECT
        order_id,
        SUM(amount) AS refund_amount
    FROM staging.refunds
    GROUP BY order_id
),

customer_rfm AS (
    SELECT
        o.customer_id,
        MAX(o.ordered_at) AS last_purchase,
        COUNT(*) AS frequency,

        SUM(
            COALESCE(p.successful_payment, 0)
            - COALESCE(r.refund_amount, 0)
        ) AS monetary

    FROM staging.orders o

    INNER JOIN payment_summary p
        ON o.order_id = p.order_id

    LEFT JOIN refund_summary r
        ON o.order_id = r.order_id

    WHERE o.order_status <> 'cancelled'

    GROUP BY o.customer_id
),

snapshot AS (
    SELECT
        MAX(ordered_at) + INTERVAL '1 day' AS snapshot_date
    FROM staging.orders
    WHERE order_status <> 'cancelled'
),

scored AS (
    SELECT
        c.*,
        s.snapshot_date,

        NTILE(4) OVER (
            ORDER BY c.last_purchase DESC
        ) AS r_score,

        NTILE(4) OVER (
            ORDER BY c.frequency ASC
        ) AS f_score,

        NTILE(4) OVER (
            ORDER BY c.monetary ASC
        ) AS m_score

    FROM customer_rfm c
    CROSS JOIN snapshot s
)

SELECT
    customer_id,
    last_purchase,
    snapshot_date::DATE - last_purchase::DATE AS recency,
    frequency,
    monetary AS historical_clv,
    r_score,
    f_score,
    m_score,

    CASE
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3
            THEN 'Champions'
        WHEN r_score >= 2 AND f_score >= 3
            THEN 'Loyal Customers'
        WHEN r_score >= 3 AND f_score >= 2
            THEN 'Potential Loyalists'
        WHEN r_score = 4 AND f_score = 1
            THEN 'New Customers'
        WHEN r_score <= 2 AND f_score >= 3
            THEN 'At Risk'
        ELSE 'Hibernating'
    END AS customer_segment

FROM scored;



SELECT *
FROM analytics.customer_analytics
LIMIT 10;


SELECT
    customer_segment,
    COUNT(*) AS total_customers
FROM analytics.customer_analytics
GROUP BY customer_segment
ORDER BY total_customers DESC;



SELECT
    'monthly_performance' AS view_name,
    COUNT(*) AS total_records
FROM analytics.monthly_performance

UNION ALL

SELECT
    'customer_analytics',
    COUNT(*)
FROM analytics.customer_analytics;
