from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from datetime import datetime, timedelta

CONNECTION_FETCHING_ID = "ad4ce0f8-1513-4118-af19-f3441db885b4"
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
    "airbyte_run",
    default_args=default_args,
    schedule_interval="0 6 * * *",  # Exécution quotidienne à 6h du matin
    catchup=False,
)

# Tâche pour exécuter dbt run
airbyte_run = AirbyteTriggerSyncOperator(
    task_id="run_airbyte_fetch",
    airbyte_conn_id="airbyte_conn",
    connection_id=CONNECTION_FETCHING_ID,
    asynchronous=False,
    dag=dag,
)

# Définition du workflow
airbyte_run
