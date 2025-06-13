from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def saludar():
    print("Hola desde Airflow!")

with DAG("dag_de_prueba", start_date=datetime(2023, 1, 1), schedule_interval=None, catchup=False) as dag:
    tarea = PythonOperator(
        task_id="saludo",
        python_callable=saludar
    )
