{{
    config(
        materialized='incremental',
        incremental_strategy='microbatch',
        event_time='order_date',
        begin='2026-01-01',
        batch_size='day',
        lookback=1,
        unique_key=['order_date', 'product_id', 'status'],
        pre_hook="DROP TABLE IF EXISTS {{ this.schema }}.{{ this.identifier }}__dbt_tmp FORCE"
    )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

joined as (
    select
        date_trunc('day', o.order_date) as order_date,
        oi.product_id,
        o.status,
        count(distinct o.order_id) as num_orders,
        sum(oi.quantity) as total_quantity,
        sum(oi.price * oi.quantity) as total_revenue
    from orders o
    join order_items oi on o.order_id = oi.order_id
    group by 1, 2, 3
)

select * from joined