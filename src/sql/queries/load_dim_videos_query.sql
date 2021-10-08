INSERT INTO dim_videos
(yt_video_id, category_id, channel_id, date_id, video_title, publish_time,
ratings_disabled, cmt_disabled, video_error_or_removed, tags, old_title, effective_date)
SELECT 
DISTINCT
v.client_video_id, 
dc.category_id,
dch.channel_id,
dd.date_id,
v.title,
v.publish_time,
v.ratings_disabled,
v.comments_disabled,
v.video_error_or_removed,
v.tags,
vtc.old_title,
vtc.effective_date
FROM videos v 
JOIN dim_category dc ON v.category_id = dc.yt_category_id
JOIN dim_channel dch ON v.channel_title = dch.channel_name
JOIN dim_publish_date dd ON v.publish_time::date = dd.publish_date
LEFT JOIN video_title_change vtc ON vtc.new_title = v.title AND vtc.yt_video_id = v.client_video_id
WHERE v.video_id IN
(SELECT video_id FROM videos 
WHERE (client_video_id, trending_date)  IN
(SELECT client_video_id, MAX(trending_date) FROM
videos GROUP BY client_video_id))
ON CONFLICT ON CONSTRAINT unique_yt_video_id DO NOTHING;