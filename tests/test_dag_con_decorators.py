from airflow.models import DagBag
from dags.dag_con_decorators import dag, generar_saludo


def test_dag_importado_sin_errores():
    """
    Verifica que no haya errores al importar DAGs desde la carpeta 'dags'.
    Esto simula cómo Airflow descubre los DAGs.
    """
    dag_bag = DagBag(dag_folder="dags", include_examples=False)
    assert len(dag_bag.import_errors) == 0, (
        f"Errores de importación: {dag_bag.import_errors}"
        )
    assert "dag_con_decorators" in dag_bag.dags


def test_dag_existe_y_tiene_tareas():
    """
    Verifica que el DAG existe y contiene tareas.
    """
    assert dag is not None
    assert len(dag.tasks) > 0
    assert dag.task_ids == ['saludar']


def test_generar_saludo():
    resultado = generar_saludo("DataOps")
    assert resultado == "¡Hola, DataOps!"
