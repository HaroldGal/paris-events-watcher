FROM apache/airflow:2.10.5

# Installer dbt et le connecteur BigQuery
RUN  pip install apache-airflow-providers-airbyte[http] \
    && pip install apache-airflow-providers-airbyte \
    && pip install dbt-bigquery
    && pip install dlt==1.15.0
    && pip install pydantic==2.11.7
    && pip install dlt[bigquery]>=1.15.0