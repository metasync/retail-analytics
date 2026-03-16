{{
    config(
        materialized='incremental',
        incremental_strategy='microbatch',
        event_time='order_date',
        begin='2026-01-01',
        batch_size='day',
        lookback=1,
        unique_key=['order_date', 'product_id', 'status'],
        on_schema_change='append_new_columns',
        pre_hook="DROP TABLE IF EXISTS {{ this.schema }}.{{ this.identifier }}__dbt_tmp FORCE"
    )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

daily_aggregated as (
    select
        date_trunc('day', o.order_date) as order_date,
        oi.product_id,
        o.status,
        count(distinct o.order_id) as num_orders,
        sum(oi.quantity) as total_quantity,
        sum(oi.price * oi.quantity) as total_revenue
    from orders o
    join order_items oi on o.order_id = oi.order_id
    group by order_date, product_id, status
),

-- Best Practice: Enriched with Dimension Data
-- By joining with the centralized dim_date, we ensure consistent reporting 
-- across the organization (e.g., standard fiscal quarters, holiday definitions).
enriched_sales as (
    select
        da.order_date,
        da.product_id,
        da.status,
        da.num_orders,
        da.total_quantity,
        da.total_revenue,
        
        -- Dimension Attributes from Master Data
        dd.day_name,
        dd.month_name,
        dd.quarter,
        dd.year,
        dd.is_weekend
        
    from daily_aggregated da
    left join {{ source('master_data', 'dim_date') }} dd
        on cast(da.order_date as date) = dd.date_day
)

select * from enriched_sales
