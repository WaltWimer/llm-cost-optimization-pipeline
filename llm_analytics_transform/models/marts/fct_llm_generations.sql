{{
    config(
        materialized='table'
    )
}}

with logs as (
    select * from {{ ref('stg_llm_logs') }}
),
models as (
    select * from {{ ref('dim_models') }}
),
users as (
    select * from {{ ref('dim_users') }}
)

select
    l.chat_id,
    u.user_key,
    m.model_key,
    l.event_timestamp,
    l.prompt_tokens,
    l.completion_tokens,
    l.total_tokens,
    l.generation_time_seconds,
    l.average_tps,
    -- Financial ROI Simulation: Assuming commercial API cost of $5.00 per million tokens
    round((l.total_tokens / 1000000.0) * 5.00, 4) as estimated_cloud_cost_usd,
    -- Local LLM inference cost is hardware amortized/power negligible (~$0.00)
    0.00 as local_infrastructure_cost_usd,
    round((l.total_tokens / 1000000.0) * 5.00, 4) as financial_savings_usd
from logs l
join users u on l.user_id = u.user_id
join models m on l.model_name = m.model_name


--The core fact table integrating performance, hardware metrics, 
--and cost-savings calculations compared to commercial APIs like GPT-4o / Claude equivalent