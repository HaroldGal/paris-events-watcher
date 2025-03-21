from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

CONNECTION_FETCHING_ID = "ad4ce0f8-1513-4118-af19-f3441db885b4"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 10)
}

dag = DAG(
    "full_run",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

airbyte_run = AirbyteTriggerSyncOperator(
    task_id="run_airbyte_fetch",
    airbyte_conn_id="airbyte_conn",
    connection_id=CONNECTION_FETCHING_ID,
    asynchronous=False,
    dag=dag,
)

dbt_run = BashOperator(
    task_id="run_dbt",
    bash_command="cd /opt/dbt_project && dbt run --profiles-dir /opt/dbt_project/.dbt",
    dag=dag,
)

# Worfklow
airbyte_run >> dbt_run
