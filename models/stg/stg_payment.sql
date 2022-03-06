WITH source AS ( SELECT * FROM public.t_payment )

SELECT
    id AS payment_id,
    order_id,
    payment_method,
    amount,
    gmt_created,
    gmt_updated
FROM source