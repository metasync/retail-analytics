
with source as (
    select * from {{ source('retail_source', 'raw_products') }}
),

renamed as (
    select
        product_id,
        name,
        category,
        price,
        updated_at,
        row_number() over (partition by product_id order by updated_at desc) as rn
    from source
)

select * except(rn) from renamed where rn = 1