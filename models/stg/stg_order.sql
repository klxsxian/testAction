WITH source AS ( SELECT * FROM public.t_order )

SELECT
    id AS order_id,
    member_id,
    real_amount,
    status,
    gmt_created,
    gmt_updated
FROM source