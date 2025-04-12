SELECT MIN(aqius) AS lowest_aqi
FROM {{ ref('stg_aqi_data') }}
WHERE local_ts >= CURRENT_DATE - INTERVAL '3 months'
