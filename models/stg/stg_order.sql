with source as ( select * from public.t_order )

select
    id as order_id,
    member_id,
    real_amount,
    status,
    gmt_created,
    gmt_updated
from source