# dsai-de-dataops
To force validar_nombres_dag.py warning:
- In scripts/validar_nombres_dag.py:
Change any dag_id to nost start with "dag_"

To force warning in generar_saludo function:
- In dags/dag_con_decorators.py: Change return f"¡Hola, {nombre}!" => return f"Hola, {nombre}!"