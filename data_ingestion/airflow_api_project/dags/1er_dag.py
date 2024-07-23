from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

with DAG(
    'example_dag',
    start_date=datetime(2024, 7, 23),
    schedule_interval='@daily', 
    catchup=False  
) as dag:
    
    op = DummyOperator(task_id='op')
