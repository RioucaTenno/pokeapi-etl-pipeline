from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'RioucaTenno',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'pokemon_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for PokeAPI',
    schedule_interval='@daily', 
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    extract_task = BashOperator(
        task_id='extract',
        bash_command='python /opt/airflow/scripts/extract.py',
    )

    transform_load_task = BashOperator(
        task_id='transform_load',
        bash_command='python /opt/airflow/scripts/transform_load.py',
    )

    extract_task >> transform_load_task