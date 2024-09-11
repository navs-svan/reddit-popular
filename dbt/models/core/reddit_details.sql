{{ config(materialized='table') }}

with ph_data as (
    select *, 
        'PH' as country 
    from {{ ref('reddit_PH') }}
), 

my_data as (
    select *,
        'MY' as country
    from {{ ref('reddit_MY') }}
),

sg_data as (
    select *,
        'SG' as country
    from {{ ref('reddit_SG') }}
),

th_data as (
    select *,
        'TH' as country
    from {{ ref('reddit_TH') }}
),

global_data as (
    select *,
        'GLOBAL' as country
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