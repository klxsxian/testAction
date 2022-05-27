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

payment AS ( SELECT * FROM {{ref('stg_payment')}}
)

SELECT
    --
    o.order_id,
    o.member_id,
    o.gmt_created AS order_gmt_created,
    o.gmt_updated AS order_gmt_update,
    o.real_amount,
    --
    p.payment_id,
    p.amount AS payment_amount,
    p.gmt_created AS payment_gmt_created,
    p.gmt_updated AS payment_gmt_updated

FROM orders as o
LEFT JOIN payment AS p ON o.order_id = p.order_id

{% if is_incremental() %}
WHERE 1 = 1
AND p.gmt_updated between '{{ var('start_date') }}' and  '{{ var('end_date') }}'
{% endif %}