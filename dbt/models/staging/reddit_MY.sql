{{ config(materialized='view') }}


select
    {{ dbt_utils.surrogate_key(['title', 'subreddit', 'author']) }} as post_id,
    title,
    subreddit,
    author,
    CONCAT('https://www.reddit.com', url) as post_url,
    nsfw,
    score,
    self_text,
    upvote_ratio,
    awards,
    timestamp_seconds(cast(time as integer)) as date_posted

from {{ source('staging', 'MY')}}

{% if var('is_test_run', default=true) %}

    limit 100

{% endif %}