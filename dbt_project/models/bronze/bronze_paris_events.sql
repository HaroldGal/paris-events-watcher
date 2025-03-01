{{ 
    config(
        materialized='table',
        incremental_strategy = 'insert_overwrite',
        unique_key='event_id',
        partition_by = {
        'field': 'event_date_start', 
        'data_type': 'timestamp',
        'granularity': 'day'
    }
   ) 
}}

SELECT 
    id as event_id, 
    url AS event_url, 
    title AS event_title,
    TIMESTAMP(date_start) AS event_date_start,
    TIMESTAMP(date_end) AS event_date_end,
    lead_text AS event_lead_text, 
    description AS event_description
FROM landing.paris_events_export