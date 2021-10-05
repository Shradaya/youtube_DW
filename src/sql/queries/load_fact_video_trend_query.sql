INSERT INTO fact_video_trend (video_id, country_id, date_id, trending_date, views, likes, dislike, cmt_count,
							 diff_publish_trend)
(SELECT 
dv.video_id,
dc.country_id,
dd.date_id,
v.trending_date,
v."views",
v.likes,
v.dislikes,
v.comment_count,
v.diff_publish_trend 
FROM videos v
JOIN dim_country dc ON v.country = dc.country_name 
JOIN dim_videos dv ON dv.yt_video_id = v.client_video_id 
JOIN dim_trending_date dd ON dd.trending_date = v.trending_date ) 