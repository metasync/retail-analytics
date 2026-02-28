
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        event_time='order_date',
        pre_hook="DROP TABLE IF EXISTS {{ this.schema }}.{{ this.identifier }}__dbt_tmp FORCE",
        post_hook="DROP TABLE IF EXISTS {{ this.schema }}.{{ this.identifier }}__dbt_tmp FORCE"
    )
}}

with source as (
    select * from {{ source('retail_source', 'raw_orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date,
        status,
        total_amount,
        items,
        current_timestamp() as dbt_updated_at
    from source
)

select * from renamed

{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    where order_id not in (select order_id from {{ this }})
{% endif %}
