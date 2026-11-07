from airflow.decorators import dag, task
from datetime import datetime


def generar_saludo(nombre):
    return f"¡Hola, {nombre}!"


@dag(
    dag_id="dag_con_decorators",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ejemplo"]
)
def flujo_de_saludo():

    @task
    def saludar():
        mensaje = generar_saludo("Airflow")
        print(mensaje)

    saludar()  # ejecución de la tarea


dag = flujo_de_saludo()
