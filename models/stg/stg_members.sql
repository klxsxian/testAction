WITH source AS ( SELECT * FROM public.t_member )

SELECT
    id AS member_id,
    name,
    address,
    gmt_created,
    gmt_updated
FROM source