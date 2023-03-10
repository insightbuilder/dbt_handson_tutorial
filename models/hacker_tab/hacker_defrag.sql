with hacker as (
  select 
    index as hacker_id,
    src,spt,srcstr,country
  from {{ source('test','hacker_data') }}
),

group_data as (
  select 
    country, count(index) as count_grp
  from {{ source('test','hacker_data') }}
  group by country 
  order by count_grp 
),

final as (
  select
    hacker.hacker_id, hacker.src, hacker.spt, 
    hacker.srcstr, group_data.country,
    group_data.count_grp
  from hacker
  left join group_data using (country)
)

select * from final

