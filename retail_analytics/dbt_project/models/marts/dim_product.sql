
{{
    config(
        materialized='incremental',
        unique_key='product_id'
    )
}}

with source as (
    select * from {{ ref('stg_products') }}
)

select
    product_id,
    name,
    category,
    price,
    updated_at,
    current_timestamp() as dbt_updated_at
from source

-- Removed tautological filter.
-- StarRocks handles upserts efficiently via Primary Key model.
