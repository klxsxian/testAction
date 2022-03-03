{{
    config(
        materialized='incremental',
        unique_key='payment_id',
        incremental_strategy='insert_overwrite'
    )
}}

with
orders as ( select * from {{ref('stg_order')}}
),

member as ( select * from {{ref('stg_members')}}
),

payment as ( select * from {{ref('stg_payment')}}
)

select
    --
    orders.order_id,
    orders.member_id,
    orders.gmt_created as order_gmt_created,
    orders.gmt_updated as order_gmt_update,
    orders.real_amount,
    --
    member.name,
    member.address,
    --
    p.payment_id,
    p.amount as payment_amount,
    p.gmt_created as payment_gmt_created,
    p.gmt_updated as payment_gmt_updated

from orders
left join member on orders.member_id = member.member_id
left join payment as p on orders.order_id = p.order_id

{% if is_incremental() %}
where 1 = 1
      and p.gmt_updated >= (select max(payment_gmt_updated) from {{ this }})
    {% endif %}