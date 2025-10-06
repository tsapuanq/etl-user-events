import os
from sqlalchemy import create_engine
import pandas as pd

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = "postgres"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}")

csv_path = "/opt/airflow/data/cleaned_user_events.csv"

with engine.begin() as conn:
    connection = conn.connection 
    cursor = connection.cursor()

    with open(csv_path, "r", encoding="utf-8") as f:
        next(f) 
        cursor.copy_expert(
            "COPY user_events FROM STDIN WITH CSV DELIMITER ',' NULL ''", f
        )

    connection.commit()
    cursor.close()

print("csv loaded to user_events")