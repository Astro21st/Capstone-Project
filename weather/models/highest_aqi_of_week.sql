SELECT MAX(aqius) AS highest_aqi
FROM {{ ref('stg_aqi_data') }}
WHERE local_ts >= date_trunc('week', CURRENT_DATE)
