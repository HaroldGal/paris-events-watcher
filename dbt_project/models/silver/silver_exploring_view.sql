{{ 
    config(
        materialized='view',
        description='Normalized view: one row per event per day, joining enriched event info with daily breakdown'
    ) 
}}

SELECT
    d.event_id,
    d.date AS event_date,
    e.event_title,
    e.event_url,
    e.event_date_start,
    e.event_date_end,
    e.event_duration,
    e.event_lead_text,
    e.clean_description,
    e.event_status,
    d.is_weekend
FROM {{ ref('silver_events_by_day') }} d
LEFT JOIN {{ ref('silver_paris_events_enriched') }} e
    ON d.event_id = e.event_id
