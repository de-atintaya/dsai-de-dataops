# dsai-de-dataops

A hands-on learning project focused on understanding **GitHub Actions** through a practical DataOps example. It uses Apache Airflow DAGs as the subject of a real CI/CD pipeline that automatically runs code quality, security, and naming-convention checks on every push or pull request.

## Project Goal

The goal is not to build a production Airflow deployment — it is to understand how a CI/CD pipeline works by seeing it in action:

- What **triggers** a pipeline run (push to `feature/**`, PR to `develop`)
- What kinds of **checks are automated** (syntax, style, tests, security, naming conventions)
- How the pipeline **fails** when code does not meet quality standards
- How a **CD job** deploys only after all CI checks pass

## Project Structure

```
dsai-de-dataops/
├── .github/
│   └── workflows/
│       └── ci_cd.yml                   # GitHub Actions pipeline definition
├── dags/
│   ├── dag_ejemplo.py                  # Basic DAG using PythonOperator
│   └── dag_con_decorators.py           # DAG using the modern @dag / @task decorator style
├── scripts/
│   └── validar_nombres_dag.py          # Custom script that enforces DAG naming conventions
├── tests/
│   ├── test_dag_ejemplo.py             # Unit tests for dag_ejemplo
│   └── test_dag_con_decorators.py      # Unit tests for dag_con_decorators
├── requirements.txt                    # Runtime dependency: Apache Airflow
└── requirements-dev.txt                # Dev tools: pytest, flake8, bandit, safety
```

## How the Pipeline Works

The pipeline is defined in `.github/workflows/ci_cd.yml` and has two jobs.

### CI — Code validation and tests

Runs on every push to a `feature/**` branch and on every PR to `develop`.

| Step | Tool | What it checks |
|------|------|----------------|
| Syntax check | `py_compile` | DAG files parse as valid Python before anything runs |
| Style linter | `flake8` | Code follows PEP 8 style guidelines (warnings only, does not fail) |
| Unit tests | `pytest` | DAG structure and business logic assertions pass |
| Naming conventions | `validar_nombres_dag.py` | All DAG IDs start with `dag_` and use only lowercase and underscores |
| Security scan | `bandit` | No common security vulnerabilities in DAG code |
| Dependency audit | `safety` | No known CVEs in `requirements.txt` packages (warnings only, does not fail) |

### CD — Simulated deployment

Runs only when a PR to `develop` passes all CI checks (`needs: ci`). The deployment steps are simulated (no real Airflow server), but they mirror a real deployment: package the DAGs, upload them to the server, and restart the service.

## Running Checks Locally

Install dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Run each check individually:

```bash
# Syntax check
python -m py_compile dags/*.py

# Style linter
flake8 dags/ tests/

# Unit tests
PYTHONPATH=$(pwd) pytest tests/

# Naming conventions
PYTHONPATH=$(pwd) python scripts/validar_nombres_dag.py

# Security scan
bandit -r dags/

# Dependency audit
safety check -r requirements.txt
```

## Breaking the Pipeline on Purpose (Learning Exercise)

One of the best ways to understand CI/CD is to deliberately make the pipeline fail, read the error in the GitHub Actions tab, fix it, and watch it pass again. Here are specific changes to trigger each check.

### Break the naming convention check

In `dags/dag_ejemplo.py`, change the `dag_id` from `"dag_de_prueba"` to a value that does not start with `dag_`, for example `"ejemplo_dag"`.

The `validar_nombres_dag.py` script will detect the violation and exit with code 1, failing the **"Validar convenciones de nombres de DAGs"** step.

### Break a unit test

In `dags/dag_con_decorators.py`, change:

```python
return f"¡Hola, {nombre}!"
```

to:

```python
return f"Hola, {nombre}!"   # missing the opening ¡ character
```

The test `test_generar_saludo` in `tests/test_dag_con_decorators.py` asserts the exact string `"¡Hola, DataOps!"`, so pytest will fail with an assertion mismatch in the **"Ejecutar pruebas unitarias"** step.

### Break the syntax check

In any DAG file, introduce a Python syntax error (for example, remove a closing parenthesis or add a stray character). `py_compile` will catch it in the **"Validar sintaxis de los DAGs"** step before any other check runs.

---

After each intentional break, commit and push to a `feature/` branch, open a PR to `develop`, and observe which step turns red in the **GitHub Actions** tab. Fix the issue, push again, and confirm the pipeline goes green.
