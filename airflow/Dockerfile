FROM apache/airflow:2.10.5

# Installer dbt et le connecteur BigQuery
RUN pip install dbt-bigquery \
    && pip install apache-airflow-providers-airbyte[http] \
    && pip install apache-airflow-providers-airbyte