
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

-- Removed tautological filter.
-- StarRocks handles upserts efficiently via Primary Key model.
