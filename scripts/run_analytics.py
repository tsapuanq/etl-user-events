import os
import pandas as pd
import psycopg2

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = "postgres"

conn = psycopg2.connect(
    dbname=database,
    user=user,
    password=password,
    host=host,
    port=5432
)

# top 3 of selling products per month
top_products_query = """
WITH ranked AS (
    SELECT
        DATE_TRUNC('month', event_time)::DATE AS month,
        product_id,
        COUNT(*) AS purchase_count,
        ROW_NUMBER() OVER (
            PARTITION BY DATE_TRUNC('month', event_time)::DATE
            ORDER BY COUNT(*) DESC
        ) AS rn
    FROM user_events
    WHERE event_type = 'purchase'
    GROUP BY 1, 2
)
SELECT month, product_id, purchase_count
FROM ranked
WHERE rn <= 3
ORDER BY month, purchase_count DESC;
"""

# top 10 users with the highest growth in purchases 
top_users_query = """
WITH monthly_purchases AS (
    SELECT
        user_id,
        DATE_TRUNC('month', event_time)::DATE AS month,
        COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchases
    FROM user_events
    GROUP BY user_id, month
),
diffs AS (
    SELECT
        user_id,
        MAX(CASE WHEN month = '2019-10-01' THEN purchases ELSE 0 END) AS oct_purchases,
        MAX(CASE WHEN month = '2019-11-01' THEN purchases ELSE 0 END) AS nov_purchases
    FROM monthly_purchases
    GROUP BY user_id
)
SELECT
    user_id,
    oct_purchases,
    nov_purchases,
    nov_purchases - oct_purchases AS delta
FROM diffs
WHERE nov_purchases > oct_purchases
ORDER BY delta DESC
LIMIT 10;
"""

# low conversion rate products with high cart additions
conversion_query = """
WITH views AS (
    SELECT product_id, COUNT(*) AS view_count
    FROM user_events
    WHERE event_type = 'view'
    GROUP BY product_id
),
carts AS (
    SELECT product_id, COUNT(*) AS cart_count
    FROM user_events
    WHERE event_type = 'cart'
    GROUP BY product_id
),
purchases AS (
    SELECT product_id, COUNT(*) AS purchase_count
    FROM user_events
    WHERE event_type = 'purchase'
    GROUP BY product_id
),
combo AS (
    SELECT
        v.product_id,
        COALESCE(v.view_count, 0) AS views,
        COALESCE(c.cart_count, 0) AS carts,
        COALESCE(p.purchase_count, 0) AS purchases
    FROM views v
    LEFT JOIN carts c ON v.product_id = c.product_id
    LEFT JOIN purchases p ON v.product_id = p.product_id
)
SELECT *
FROM combo
WHERE purchases < 10 AND carts > 50
ORDER BY carts DESC;
"""

queries = {
    "top_3_products.csv": top_products_query,
    "top_10_users_growth.csv": top_users_query,
    "low_conversion_high_cart.csv": conversion_query
}

for filename, query in queries.items():
    df = pd.read_sql(query, conn)
    df.to_csv(f"data/{filename}", index=False)

conn.close()