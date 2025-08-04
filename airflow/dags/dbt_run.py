"""
Take care about your creadentials in the --profiles-dir /opt/dbt_project/.dbt
If you use docker, it is a volume connected to the host machine, ~/.dbt (see dockerfile-compose of airflow)
These credentials path should be coherent with the path on the docker container.
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 10), 
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "dbt_run_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

dbt_run = BashOperator(
    task_id="run_dbt",
    bash_command="cd /opt/dbt_project && dbt run --profiles-dir /opt/dbt_project/.dbt",
    dag=dag,
)

dbt_run
