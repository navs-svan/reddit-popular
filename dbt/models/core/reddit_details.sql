{{ config(materialized='table') }}

with ph_data as (
    select *, 
        'Philippines' as country 
    from {{ ref('reddit_PH') }}
), 

my_data as (
    select *,
        'Malaysia' as country
    from {{ ref('reddit_MY') }}
),

sg_data as (
    select *,
        'Singapore' as country
    from {{ ref('reddit_SG') }}
),

th_data as (
    select *,
        'Thailand' as country
    from {{ ref('reddit_TH') }}
),

global_data as (
    select *,
        'Global' as country
    from {{ ref('reddit_global') }}
),


data_union as (
    
    select * from ph_data
    union all 
    select * from my_data
    union all 
    select * from sg_data
    union all
    select * from th_data
    union all
    select * from global_data

)

select *
from data_union