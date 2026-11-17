{{
    config(
        materialized='table'
    )
}}

select
    row_number() over (order by user_id) as user_key,
    user_id,
    count(chat_id) as total_requests_made
from {{ ref('stg_llm_logs') }}
group by user_id





-- (Extracts unique active corporate users/developers)