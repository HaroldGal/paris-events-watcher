from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from datetime import datetime, timedelta
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


CONNECTION_FETCHING_ID = "ad4ce0f8-1513-4118-af19-f3441db885b4"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 10),
    "retries": 0
}

dag = DAG(
    "airbyte_run",
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

dbt_trigger = TriggerDagRunOperator(
    task_id="trigger_dbt_run",
    trigger_dag_id="dbt_run_pipeline_decomposed",
    wait_for_completion=False,
    reset_dag_run=True,
    dag=dag,
)

airbyte_run >> dbt_trigger
