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

{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    where product_id in (select product_id from source)
{% endif %}