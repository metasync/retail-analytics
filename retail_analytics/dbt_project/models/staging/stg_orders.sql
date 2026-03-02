
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

-- No manual filter needed: StarRocks Primary Key table handles upserts automatically based on unique_key.
-- If using 'append' strategy (Duplicate Key), we might need a filter, but 'incremental' usually implies unique_key merge.
