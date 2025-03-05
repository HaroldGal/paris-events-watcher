{{ config(
    materialized='table',
    schema='gold'
) }}

SELECT *
FROM {{ ref('gold_paris_events_daily') }}
WHERE DATE(event_date) BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 7 DAY)
AND event_duration < 7