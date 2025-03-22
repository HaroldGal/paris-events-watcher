import os
import json
from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

CONNECTION_FETCHING_ID = "ad4ce0f8-1513-4118-af19-f3441db885b4"
dbt_path = "/opt/dbt_project"
manifest_file = os.path.join(dbt_path, "target/manifest.json")

with open(manifest_file) as f:
    manifest = json.load(f)
    dbt_nodes = manifest["nodes"]

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

dbt_tasks = {}
for node_id, node_info in dbt_nodes.items():
    dbt_tasks[node_id] = BashOperator(
            task_id=f"run_dbt_{node_id}",
            bash_command=f"cd {dbt_path} && dbt run --models {node_info['name']} --profiles-dir {dbt_path}/.dbt",
            dag=dag,
        )
    
for node_id, node_info in dbt_nodes.items():
    upstream_nodes = node_info["depends_on"]["nodes"]
    if upstream_nodes:
        for upstream_node in upstream_nodes:
            dbt_tasks[upstream_node] >> dbt_tasks[node_id]
    else:
        airbyte_run >> dbt_tasks[node_id]

"""dbt_run = BashOperator(
    task_id="run_dbt",
    bash_command="cd /opt/dbt_project && dbt run --profiles-dir /opt/dbt_project/.dbt",
    dag=dag,
)"""
