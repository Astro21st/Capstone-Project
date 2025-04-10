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

def _get_aqi_data():
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
    print(json.dumps(data, indent=2))

    with open(f"{DAG_FOLDER}/aqi_data.json", "w") as f:
        json.dump(data, f)

def _create_table():
    pg_hook = PostgresHook(postgres_conn_id="weather_postgres_conn", schema="postgres")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS aqi_data (
        ts TIMESTAMP PRIMARY KEY,
        city TEXT,
        state TEXT,
        country TEXT,
        aqius INTEGER,
        mainus TEXT,
        aqicn INTEGER,
        maincn TEXT,
        tp FLOAT,
        pr FLOAT,
        hu FLOAT,
        ws FLOAT,
        wd INTEGER,
        ic TEXT
    );
    """
    cursor.execute(sql)
    connection.commit()

def _load_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id="weather_postgres_conn", schema="postgres")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    with open(f"{DAG_FOLDER}/aqi_data.json", "r") as f:
        data = json.load(f)["data"]

    ts = data["current"]["pollution"]["ts"]
    city = data["city"]
    state = data["state"]
    country = data["country"]
    aqius = data["current"]["pollution"]["aqius"]
    mainus = data["current"]["pollution"]["mainus"]
    aqicn = data["current"]["pollution"]["aqicn"]
    maincn = data["current"]["pollution"]["maincn"]

    weather = data["current"]["weather"]
    tp = weather["tp"]
    pr = weather["pr"]
    hu = weather["hu"]
    ws = weather["ws"]
    wd = weather["wd"]
    ic = weather["ic"]

    sql = """
        INSERT INTO aqi_data (ts, city, state, country, aqius, mainus, aqicn, maincn, tp, pr, hu, ws, wd, ic)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ts) DO NOTHING;
    """
    cursor.execute(sql, (ts, city, state, country, aqius, mainus, aqicn, maincn, tp, pr, hu, ws, wd, ic))
    connection.commit()

default_args = {
    "email": ["pipe@dpu.team"],
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    "airvisual_aqi_dag",
    default_args=default_args,
    schedule="0 */1 * * *",  # Every 3 hours
    start_date=timezone.datetime(2025, 4, 10, 0, 0),
    tags=["dpu", "airvisual"],
):

    start = EmptyOperator(task_id="start")

    get_aqi_data = PythonOperator(
        task_id="get_aqi_data",
        python_callable=_get_aqi_data,
    )

    create_table = PythonOperator(
        task_id="create_table",
        python_callable=_create_table,
    )

    load_data = PythonOperator(
        task_id="load_data_to_postgres",
        python_callable=_load_to_postgres,
    )

    send_email = EmailOperator(
        task_id="send_email",
        to=["pipe@dpu.team"],
        subject="AQI Data Pipeline Finished",
        html_content="The AirVisual AQI pipeline has successfully run.",
    )

    end = EmptyOperator(task_id="end")

    start >> get_aqi_data >> load_data >> send_email >> end
    start >> create_table >> load_data
