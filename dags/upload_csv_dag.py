from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_script(script_name):
    subprocess.run(['python', f'scripts/{script_name}'], check=True)

with DAG(
    dag_id="init_and_load_user_events",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False) as dag:

    init_table = PythonOperator(
        task_id="init_table",
        python_callable=run_script,
        op_args=["init_table.py"])

    clean_data = PythonOperator(
        task_id="clean_data",
        python_callable=run_script,
        op_args=["clean_data.py"])

    load_csv = PythonOperator(
        task_id="load_csv",
        python_callable=run_script,
        op_args=["load_to_postgres.py"])

    run_analytics = PythonOperator(
    task_id="run_analytics",
    python_callable=run_script,
    op_args=["run_analytics.py"])

    init_table >> clean_data >> load_csv >> run_analytics