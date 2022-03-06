{{
    config(
        materialized='incremental',
        unique_key='payment_id',
        incremental_strategy='insert_overwrite'
    )
}}

WITH
orders AS ( SELECT * FROM {{ref('stg_order')}}
),

member AS ( SELECT * FROM {{ref('stg_members')}}
),

payment AS ( SELECT * FROM {{ref('stg_payment')}}
)

SELECT
    --
    orders.order_id,
    orders.member_id,
    orders.gmt_created AS order_gmt_created,
    orders.gmt_updated AS order_gmt_update,
    orders.real_amount,
    --
    member.name,
    member.address,
    --
    p.payment_id,
    p.amount AS payment_amount,
    p.gmt_created AS payment_gmt_created,
    p.gmt_updated AS payment_gmt_updated,
    TO_CHAR(NOW(), 'YYYY-MM-DD HH:MI:SS') AS updatetime

FROM orders
LEFT JOIN member ON orders.member_id = member.member_id
LEFT JOIN payment AS p ON orders.order_id = p.order_id

{% if is_incremental() %}
WHERE 1 = 1
      AND p.gmt_updated >= (SELECT MAX(payment_gmt_updated) FROM {{ this }})
    {% endif %}