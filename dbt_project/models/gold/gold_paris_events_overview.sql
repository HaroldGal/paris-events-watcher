{{ config(
    materialized='table',
    schema='gold'
) }}

WITH events AS (
    SELECT 
        event_id,
        event_status
    FROM {{ ref('silver_paris_events_enriched') }}
)

SELECT
    COUNT(*) AS total_events,
    COUNTIF(event_status = 'upcoming') AS upcoming_events,
    COUNTIF(event_status = 'ongoing') AS ongoing_events,
    COUNTIF(event_status = 'past') AS past_events
FROM events