{{
    config(
        materialized='incremental',
        unique_key='customer_id'
    )
}}

with source as (
    select * from {{ ref('stg_customers') }}
)

select
    customer_id,
    first_name,
    last_name,
    email,
    city,
    country,
    created_at,
    current_timestamp() as dbt_updated_at
from source

{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    -- standard incremental strategy: upsert based on customer_id
    where customer_id in (select customer_id from source)
{% endif %}