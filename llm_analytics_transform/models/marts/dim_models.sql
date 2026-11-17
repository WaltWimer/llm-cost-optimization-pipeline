{{
    config(
        materialized='table'
    )
}}

select
    row_number() over (order by model_name) as model_key,
    model_name,
    case 
        when model_name like '%14b%' or model_name like '%12b%' then 'High Parameters (Medium Speed)'
        else 'Standard Parameters (High Speed)'
    end as model_tier,
    avg(average_tps) as avg_observed_tps
from {{ ref('stg_llm_logs') }}
group by model_name



--(Extracts unique models and establishes baseline hardware metrics)