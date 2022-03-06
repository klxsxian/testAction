with source as ( select * from public.t_member )
select
    id as member_id,
    name,
    address,
    gmt_created,
    gmt_updated
from source