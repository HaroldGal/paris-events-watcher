from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configuration générale du DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 10),  # Date de départ
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Définition du DAG
dag = DAG(
    "dbt_run_pipeline",
    default_args=default_args,
    schedule_interval="0 6 * * *",  # Exécution quotidienne à 6h du matin
    catchup=False,
)

# Tâche pour exécuter dbt run
dbt_run = BashOperator(
    task_id="run_dbt",
    bash_command="cd /opt/dbt_project && dbt run --profiles-dir /opt/dbt_project/.dbt",
    dag=dag,
)

# Définition du workflow
dbt_run
