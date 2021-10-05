INSERT INTO videos(client_video_id, trending_date, title, channel_title, category_id, publish_time, tags, views, likes, dislikes,
comment_count, comments_disabled, ratings_disabled, video_error_or_removed, country, diff_publish_trend)
SELECT 
video_id, 
TO_DATE(trending_date, 'YY.DD.MM') AS trending_date, 
title, 
channel_title, 
category_id, 
CAST(publish_time AS TIMESTAMP), 
tags, 
CAST(views AS INT), 
CAST(likes AS INT),
CAST(dislikes AS INT), 
CAST(comment_count AS INT),
CAST(comments_disabled AS BOOLEAN),
CAST(ratings_disabled AS BOOLEAN),
CAST(video_error_or_removed AS BOOLEAN),  
country,
TO_DATE(trending_date, 'YY.DD.MM') - publish_time::TIMESTAMP::DATE
FROM raw_videos WHERE video_id <> '#NAME?';