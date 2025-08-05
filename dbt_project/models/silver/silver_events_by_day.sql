{{ 
    config(
        materialized='table',
        incremental_strategy = 'insert_overwrite',
        partition_by = {
        'field': 'date', 
        'data_type': 'timestamp',
        'granularity': 'month'
    }
   ) 
}}


WITH date_series AS (
    -- Generate a list of all dates within the event period
    SELECT 
        event_id, 
        date_add(event_date_start, INTERVAL n DAY) AS date
    FROM {{ ref('bronze_paris_events') }}
    CROSS JOIN UNNEST(GENERATE_ARRAY(0, DATE_DIFF(event_date_end, event_date_start, DAY))) AS n
)

SELECT 
    date,
    event_id,
    IF(EXTRACT(DAYOFWEEK FROM date) IN (1, 7), TRUE, FALSE) AS is_weekend
FROM date_series