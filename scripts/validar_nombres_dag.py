import re
from airflow.models import DagBag

# Regex: nombre debe empezar con dag_, solo minúsculas y guiones bajos
PATRON_NOMBRE = re.compile(r"^dag_[a-z0-9_]+$")

def main():
    dag_bag = DagBag(dag_folder="dags", include_examples=False)

    errores = []
    for dag_id in dag_bag.dags:
        if not PATRON_NOMBRE.match(dag_id):
            errores.append(dag_id)

    if errores:
        print("Los siguientes DAGs no cumplen con la convención de nombres:")
        for e in errores:
            print(f" - {e}")
        exit(1)  # Falla el pipeline
    else:
        print("Todos los DAGs cumplen con la convención de nombres.")

if __name__ == "__main__":
    main()
