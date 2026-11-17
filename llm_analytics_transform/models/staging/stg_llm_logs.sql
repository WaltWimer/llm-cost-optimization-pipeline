with source as (
    select * from {{ source('RAW', 'RAW_LLM_LOGS') }}
),

renamed as (
    select
        chat_id as chat_id,
        user_id as user_id,
        event_timestamp as event_timestamp,
        model_name as model_name,
        prompt_tokens as prompt_tokens,
        completion_tokens as completion_tokens,
        generation_time_seconds as generation_time_seconds,
        average_tps as average_tps,
        -- Business logic: Total tokens per request
        (prompt_tokens + completion_tokens) as total_tokens
    from source
)

select * from renamed