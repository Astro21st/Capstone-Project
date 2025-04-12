SELECT ROUND(AVG(aqius), 2) AS average_aqi
FROM {{ ref('stg_aqi_data') }}
WHERE local_ts >= date_trunc('week', CURRENT_DATE)
