{{ config(
    materialized='table',
    schema='gold'
) }}

SELECT *
FROM {{ ref('silver_exploring_view') }}
WHERE DATE(event_date) BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 7 DAY)
AND DATE(event_date_end) <= DATE_ADD(CURRENT_DATE(), INTERVAL 7 DAY)