with source as ( select * from public.t_payment )

select
    id as payment_id,
    order_id,
    payment_method,
    amount,
    gmt_created,
    gmt_updated
from source
