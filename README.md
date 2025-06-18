# 📍 My Capstone Project
# Author: Chatmongkol Tussabut

# 🎓 Capstone Project: Bangkok Air Quality Data Pipeline

## 🎯 Objective

This project aims to build a data pipeline that automatically extracts **Air Quality Index (AQI)** data for **Bangkok** from the [AirVisual API](https://www.iqair.com/th-en/), transforms it into a clean and structured format, and loads it into a **PostgreSQL** database.  
The pipeline supports daily air quality monitoring and enables data-driven decision-making through SQL analytics and dashboard-ready models.

---

## 🧱 Components

| Component        | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **Apache Airflow** | Orchestrates the ETL pipeline (scheduled every 1 hours)                   |
| **PostgreSQL**     | Stores raw and transformed AQI data                                        |
| **dbt (Optional)** | Performs SQL-based data modeling and transformation                        |
| **AirVisual API**  | Provides real-time AQI and weather data for Bangkok                        |

---

## 🔄 Pipeline Overview

- **Extract**: Scheduled Airflow DAG fetches real-time AQI and weather data from AirVisual API  
- **Transform**: JSON is flattened and filtered (e.g. `aqius`, `mainus`, `tp`, `hu`)  
- **Load**: Cleaned data inserted into `aqi_data` table with unique timestamp  
- **Modeling**: Optional dbt models build `daily` and `weekly` summary tables  
- **Monitoring**: Email is sent on successful load

---

## 📊 Business Questions Answered

1. ✅ What is the **average AQI** this week?  
2. ✅ What is the **highest AQI** in the current week?  
3. ✅ What is the **highest average AQI** in the last 3 months?  
4. ✅ What is the **lowest AQI** in the last 3 months?  
5. ✅ What are the **daily AQI summaries** (max, min, average) over the past 7 days?

---

## 🧮 Data Model: `aqi_data`

| Column      | Description                                |
|-------------|--------------------------------------------|
| `ts`        | Timestamp of the data (UTC)                |
| `city`      | City name                                  |
| `state`     | Province/region                            |
| `country`   | Country                                     |
| `aqius`     | AQI (US standard)                          |
| `mainus`    | Main pollutant (US standard)               |
| `aqicn`     | AQI (China standard)                       |
| `maincn`    | Main pollutant (China standard)            |
| `tp`, `pr`, `hu` | Temperature, pressure, humidity       |
| `ws`, `wd`, `ic` | Wind speed, wind direction, weather icon |

---

## ⚙️ Set up

### Step 1: Airflow Setup (with Docker)

```bash
# 1. Clone Airflow docker setup
curl -LfO https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml

# 2. Create necessary folders
mkdir -p ./dags ./logs ./plugins ./config

# 3. Set AIRFLOW_UID
echo -e "AIRFLOW_UID=$(id -u)" > .env

# 4. (Optional fix for some systems)
echo "AIRFLOW_UID=50000" > .env

# 5. Initialize Airflow
docker compose up airflow-init

# 6. Start Airflow
docker compose up
```
### Step 2: dbt Setup

```bash
# 1. Install dbt
pip install dbt-core dbt-postgres

# 2. Initialize dbt project
dbt init

# 3. Move profile config
mv /home/codespace/.dbt/profiles.yml weather/

# 4. Restart DB (after schema changes)
docker compose restart db

# 5. Shutdown DB
docker compose down db

# 6. Start DB in background
docker compose up db -d
```
### Note

```bash
dbt show -s "model_name"   # show specific model
dbt run                    # run all models
dbt run -t production      # run all models on production
```
