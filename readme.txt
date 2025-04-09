My name is Chatmongkol Tussabut
This is my capstone project

step 1
setup airflow + docker

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