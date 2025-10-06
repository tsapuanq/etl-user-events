import pandas as pd

input_path = "/opt/airflow/data/data.csv"  
output_path = "/opt/airflow/data/cleaned_user_events.csv"

# Только нужные колонки
use_columns = [
    'event_time', 'event_type', 'product_id', 'category_id',
    'category_code', 'brand', 'price', 'user_id', 'user_session'
]

chunksize = 50_000
first_chunk = True

for chunk in pd.read_csv(input_path, chunksize=chunksize, usecols=use_columns):
    chunk['brand'].fillna('unknown', inplace=True)
    chunk['category_code'].fillna('unknown', inplace=True)
    chunk.dropna(subset=['user_session'], inplace=True)

    chunk.to_csv(
        output_path,
        mode='w' if first_chunk else 'a',
        header=first_chunk,
        index=False
    )

    first_chunk = False