{{
    config(
        materialized='incremental',
        unique_key=['order_id', 'product_id']
    )
}}

with source as (
    select 
        order_id,
        items
    from {{ ref('stg_orders') }}
    {% if is_incremental() %}
    where dbt_updated_at > (select max(dbt_updated_at) from {{ this }})
    {% endif %}
),

flattened as (
    select
        order_id,
        get_json_string(item, '$.product_id') as product_id,
        cast(get_json_string(item, '$.quantity') as int) as quantity,
        cast(get_json_string(item, '$.price') as double) as price
    from source,
    unnest(cast(json_query(items, '$') as array<json>)) as t(item)
)

select 
    order_id,
    product_id,
    quantity,
    price,
    current_timestamp() as dbt_updated_at
from flattened