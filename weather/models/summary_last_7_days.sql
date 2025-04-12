SELECT 
  DATE(local_ts) AS date,
  MAX(aqius) AS max_aqi,
  MIN(aqius) AS min_aqi,
  ROUND(AVG(aqius), 2) AS avg_aqi
FROM {{ ref('stg_aqi_data') }}
WHERE local_ts >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(local_ts)
ORDER BY date
