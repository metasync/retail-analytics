
with source as (
    select * from {{ source('retail_source', 'raw_customers') }}
),

renamed as (
    select
        customer_id,
        first_name,
        last_name,
        email,
        city,
        country,
        created_at,
        row_number() over (partition by customer_id order by created_at desc) as rn
    from source
)

select * except(rn) from renamed where rn = 1