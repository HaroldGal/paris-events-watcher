{{ 
    config(
        materialized='table',
        incremental_strategy = 'merge',
        unique_key='event_id',
        partition_by = {
        'field': 'event_date_start', 
        'data_type': 'timestamp',
        'granularity': 'day'
    }
   ) 
}}


WITH bronze_events AS (
    SELECT 
        event_id,
        event_title,
        event_url,
        event_date_start,
        event_date_end,
        SAFE_CAST(TIMESTAMP_DIFF(event_date_end, event_date_start, DAY) AS INT64) AS event_duration,
        event_lead_text,
        REGEXP_REPLACE(event_description, r'<[^>]*>', '') AS clean_description, -- Suppression HTML
        CASE 
            WHEN TIMESTAMP(event_date_start) > CURRENT_TIMESTAMP() THEN 'upcoming'
            WHEN TIMESTAMP(event_date_start) <= CURRENT_TIMESTAMP() AND TIMESTAMP(event_date_end) >= CURRENT_TIMESTAMP() THEN 'ongoing'
            ELSE 'past'
        END AS event_status
    FROM {{ ref('bronze_paris_events') }}
),
date_series AS (
    -- Generate a list of all dates within the event period
    SELECT 
        event_id, 
        date_add(event_date_start, INTERVAL n DAY) AS event_date
    FROM {{ ref('bronze_paris_events') }}
    CROSS JOIN UNNEST(GENERATE_ARRAY(0, DATE_DIFF(event_date_end, event_date_start, DAY))) AS n
),
weekend_check AS (
    -- Check if any date in the range falls on a Saturday (7) or Sunday (1)
    SELECT 
        event_id,
        MAX(CASE WHEN EXTRACT(DAYOFWEEK FROM event_date) IN (1, 7) THEN 1 ELSE 0 END) AS overlaps_weekend
    FROM date_series
    GROUP BY event_id
)

SELECT 
    bronze_events.*,
    CAST(weekend_check.overlaps_weekend AS BOOLEAN) AS is_weekend
FROM bronze_events
LEFT JOIN weekend_check 
ON bronze_events.event_id = weekend_check.event_id