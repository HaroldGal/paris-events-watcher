import dlt
from dlt.sources.rest_api import rest_api_source
from dlt.sources.helpers.rest_client.paginators import OffsetPaginator 

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator



def load_paris_events_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_paris_events_data",
        destination='bigquery',
        dataset_name="dlt_export"
    )

    paris_events_data_source = rest_api_source(
        {
            "client": {
                "base_url": "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/que-faire-a-paris-/exports/",
                "paginator": OffsetPaginator(
                    limit=1000,
                    total_path=None
                )

            },
            "resources": [
                {
                    "name": "json",
                    "endpoint": {
                        "path": "json",
                        "params": {
                            "select": "id,url,title,lead_text,description,date_start,date_end",
                            "where": 'updated_at > "2025-01-01T00:00:00+00:00"',
                        },
                    },
                    "write_disposition": "replace",
                }
            ],
        }
    )

    load_info = pipeline.run(paris_events_data_source)
    print(load_info)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 10),
    "retries": 0
}

dag = DAG(
    "dlt_run",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

dlt_run = PythonOperator(
    task_id="dlt_run_pipeline",
    python_callable=load_paris_events_data,
    dag=dag,
)

dbt_trigger = TriggerDagRunOperator(
    task_id="trigger_dbt_run",
    trigger_dag_id="dbt_run_pipeline_decomposed",
    wait_for_completion=False,
    reset_dag_run=True,
    dag=dag,
)

dlt_run >> dbt_trigger
