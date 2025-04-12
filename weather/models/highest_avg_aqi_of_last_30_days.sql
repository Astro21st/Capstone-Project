SELECT DATE(local_ts) AS day, ROUND(AVG(aqius), 2) AS avg_aqi
FROM {{ ref('stg_aqi_data') }}
WHERE local_ts >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(local_ts)
ORDER BY avg_aqi DESC
LIMIT 1
