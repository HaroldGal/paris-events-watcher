{{ config(
    materialized='table',
    schema='gold'
) }}

WITH events AS (
    SELECT 
        event_id,
        event_title,
        event_url,
        event_duration,
        DATE(event_date_start) AS event_start,
        DATE(event_date_end) AS event_end,
        event_lead_text,
        clean_description
    FROM {{ ref('silver_paris_events_enriched') }}
),

date_series AS (
    -- Générer une ligne par jour entre event_start et event_end
    SELECT 
        e.event_id,
        DATE_ADD(e.event_start, INTERVAL n DAY) AS event_date,
        e.event_title,
        e.event_url,
        e.event_duration,
        e.event_lead_text,
        e.clean_description
    FROM events e
    CROSS JOIN UNNEST(GENERATE_ARRAY(0, DATE_DIFF(e.event_end, e.event_start, DAY))) AS n
)

SELECT * 
FROM date_series