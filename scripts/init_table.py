from sqlalchemy import create_engine, text
import os

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = "postgres"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}")

sql = """
CREATE TABLE IF NOT EXISTS user_events (
    event_time TIMESTAMP,
    event_type TEXT,
    product_id BIGINT,
    category_id BIGINT,
    category_code TEXT,
    brand TEXT,
    price NUMERIC,
    user_id BIGINT,
    user_session TEXT
);
"""

with engine.begin() as conn:
    conn.execute(text(sql))