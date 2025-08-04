"""
Take care about your creadentials in the --profiles-dir /opt/dbt_project/.dbt
If you use docker, it is a volume connected to the host machine, ~/.dbt (see dockerfile-compose of airflow)
These credentials path should be coherent with the path on the docker container.
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import json

CONNECTION_FETCHING_ID = "ad4ce0f8-1513-4118-af19-f3441db885b4"
dbt_path = "/opt/dbt_project"
manifest_file = os.path.join(dbt_path, "target/manifest.json")

# parse manifest files to break dbt nodes steps into airflow tasks
with open(manifest_file) as f:
    manifest = json.load(f)
    dbt_nodes = manifest["nodes"]

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 10), 
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "dbt_run_pipeline_decomposed",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
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
