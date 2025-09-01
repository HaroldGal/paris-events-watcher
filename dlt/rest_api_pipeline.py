import dlt
from dlt.sources.rest_api import rest_api_source
from dlt.sources.helpers.rest_client.paginators import OffsetPaginator

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


if __name__ == "__main__":
    load_paris_events_data()
