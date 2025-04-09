import json
from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils import timezone

import requests


DAG_FOLDER = "/opt/airflow/dags"


def _get_weather_data():

    API_KEY = Variable.get("air_quality_api_key")

    url = 'https://api.airvisual.com/v2/city'

    params = {
        'city': 'Bangkok',
        'state': 'Bangkok',
        'country': 'Thailand',
        'key': API_KEY
    }

    
    response = requests.get(url, params=params)
    print(response.url)

    data = response.json()
    print(data)

    with open(f"{DAG_FOLDER}/data.json", "w") as f:
        json.dump(data, f)


# def _validate_data():
#     with open(f"{DAG_FOLDER}/data.json", "r") as f:
#         data = json.load(f)

#     assert data.get("main") is not None

# def _validate_temperature_range():
#     with open(f"{DAG_FOLDER}/data.json", "r") as f:
#         data = json.load(f)

#     assert data.get("main").get("temp") >= 20
#     assert data.get("main").get("temp") <= 45

# def _create_weather_table():
#     pg_hook = PostgresHook(
#         postgres_conn_id="weather_postgres_conn",
#         schema="postgres"
#     )
#     connection = pg_hook.get_conn()
#     cursor = connection.cursor()

#     sql = """
#         CREATE TABLE IF NOT EXISTS weathers (
#             dt BIGINT NOT NULL,
#             temp FLOAT NOT NULL,
#             feels_like FLOAT
#         )
#     """
#     cursor.execute(sql)
#     connection.commit()


# def _load_data_to_postgres():
#     pg_hook = PostgresHook(
#         postgres_conn_id="weather_postgres_conn",
#         schema="postgres"
#     )
#     connection = pg_hook.get_conn()
#     cursor = connection.cursor()

#     with open(f"{DAG_FOLDER}/data.json", "r") as f:
#         data = json.load(f)

#     temp = data["main"]["temp"]
#     feels_like = data["main"]["feels_like"]
#     dt = data["dt"]
#     sql = f"""
#         INSERT INTO weathers (dt, temp, feels_like) VALUES ({dt}, {temp}, {feels_like})
#     """
#     cursor.execute(sql)
#     connection.commit()


default_args = {
    "email": ["pipe@dpu.team"],
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
}
with DAG(
    "capstone_project_dag",
    default_args=default_args,
    schedule="0 */3 * * *",
    start_date=timezone.datetime(2025, 4, 9),
    tags=["dpu"],
):
    start = EmptyOperator(task_id="start")

    get_weather_data = PythonOperator(
        task_id="get_weather_data",
        python_callable=_get_weather_data,
    )

    # validate_data = PythonOperator(
    #     task_id="validate_data",
    #     python_callable=_validate_data,
    # )

    # validate_temperature_range = PythonOperator(
    #     task_id="validate_temperature_range",
    #     python_callable=_validate_temperature_range,
    # )

    # create_weather_table = PythonOperator(
    #     task_id="create_weather_table",
    #     python_callable=_create_weather_table,
    # )

    # load_data_to_postgres = PythonOperator(
    #     task_id="load_data_to_postgres",
    #     python_callable=_load_data_to_postgres,
    # )

    # send_email = EmailOperator(
    #     task_id="send_email",
    #     to=["pipe@dpu.team"],
    #     subject="Finished getting open weather data",
    #     html_content="Done",
    # )

    end = EmptyOperator(task_id="end")

    # start >> get_weather_data >> [validate_data, validate_temperature_range] >> load_data_to_postgres >> send_email
    # start >> create_weather_table >> load_data_to_postgres
    # send_email >> end
    start >> get_weather_data >> end