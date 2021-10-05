INSERT INTO dim_videos
(yt_video_id, category_id, channel_id, date_id, video_title, publish_time,
ratings_disabled, cmt_disabled, video_error_or_removed, tags)
SELECT 
v.client_video_id, 
dc.category_id,
dch.channel_id,
dd.date_id,
v.title,
v.publish_time,
v.ratings_disabled,
v.comments_disabled,
v.video_error_or_removed,
v.tags 
FROM videos v 
JOIN dim_category dc ON v.category_id = dc.yt_category_id
JOIN dim_channel dch ON v.channel_title = dch.channel_name
JOIN dim_publish_date dd ON v.publish_time::date = dd.full_date
WHERE v.video_id IN
(SELECT video_id FROM videos 
WHERE (client_video_id, trending_date)  IN
(SELECT client_video_id, MAX(trending_date) FROM
videos
GROUP BY client_video_id))
