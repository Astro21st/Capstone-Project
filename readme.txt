My name is Chatmongkol Tussabut
This is my capstone project

step 1
setup airflow + docker download code here: https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml

1. create docker-compose.yaml

# create these airflow folder
2. mkdir -p ./dags ./logs ./plugins ./config 

# create .env
3. echo -e "AIRFLOW_UID=$(id -u)" > .env

4. enter "AIRFLOW_UID=50000" into .env

#Initialize
5. docker compose up airflow-init

#Running Airflow
6. docker compose up

step 2
setup dbt

#install dbt
1. pip install dbt-core dbt-postgres

#Initialize
2. dbt init

#move profiles.yml to weather/
3. mv /home/codespace/.dbt/profiles.yml weather/

#restart db
4. docker compose restart db

#shutdown db
5. docker compose down db

#start db on background
6 docker compose up db -d

#note
- dbt show -s "*****" // show model
- dbt run // run dbt