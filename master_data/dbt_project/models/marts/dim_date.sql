{{ config(
    materialized='table',
    unique_key='date_day'
) }}

with digits as (
    select 0 as d union all select 1 union all select 2 union all select 3 union all
    select 4 union all select 5 union all select 6 union all select 7 union all
    select 8 union all select 9
),
numbers as (
    select 
        d1.d + (d2.d * 10) + (d3.d * 100) + (d4.d * 1000) as num
    from digits d1
    cross join digits d2
    cross join digits d3
    cross join digits d4
    -- Generates 0 to 9999 (enough for ~27 years)
),
dates as (
    select 
        date_add(cast('2020-01-01' as date), interval num day) as date_day
    from numbers
    where date_add(cast('2020-01-01' as date), interval num day) < cast('2030-01-01' as date)
)
select 
    date_day,
    year(date_day) as year,
    month(date_day) as month,
    monthname(date_day) as month_name,
    day(date_day) as day_of_month,
    dayname(date_day) as day_name,
    quarter(date_day) as quarter,
    case when dayofweek(date_day) in (1, 7) then true else false end as is_weekend
from dates
