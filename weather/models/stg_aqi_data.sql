-- models/stg_aqi_data.sql
SELECT
    ts AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Bangkok' AS local_ts,
    city,
    state,
    country,
    aqius,
    mainus,
    aqicn,
    maincn,
    tp,
    pr,
    hu,
    ws,
    wd,
    ic
FROM {{ source('dpu', 'aqi_data') }}
WHERE aqius IS NOT NULL
