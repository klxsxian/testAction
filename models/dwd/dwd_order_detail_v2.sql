{{
    config(
        materialized='incremental',
        unique_key='payment_id',
        incremental_strategy='insert_overwrite'
    )
}}

with
orders as  ( select * from {{ref('stg_order')}}   ),
member as  ( select * from {{ref('stg_members')}} ),
payment as ( select * from {{ref('stg_payment')}} )

select
    --
    o.order_id,
    o.member_id,
    o.gmt_created as order_gmt_created,
    o.gmt_updated as order_gmt_update,
    o.real_amount,
    --
    m.name,
    m.address,
    --
    p.payment_id,
    p.amount as payment_amount,
    p.gmt_created as payment_gmt_created,
    p.gmt_updated as payment_gmt_updated

from orders o
         left join member m on o.member_id = m.member_id
         left join payment p on o.order_id = p.order_id

    {% if is_incremental() %}
where 1=1
  and p.gmt_updated >= (select max(payment_gmt_updated) from {{ this }})
    {% endif %}