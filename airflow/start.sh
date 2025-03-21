docker compose up airflow-init

sleep 5

docker-compose build
docker compose up

sleep 20

docker network create myNetwork
docker network connect myNetwork airbyte-abctl-control-plane
docker network connect myNetwork airflow-airflow-webserver-1
docker network connect myNetwork airflow-postgres-1
docker network connect myNetwork airflow-redis-1
docker network connect myNetwork airflow-airflow-triggerer-1
docker network connect myNetwork airflow-airflow-scheduler-1
docker network connect myNetwork airflow-airflow-worker-1