INSERT INTO video_title_change (old_title, new_title, effective_date)
WITH cte as
(SELECT 
v.client_video_id, v.title old_title, v1.title new_title, MIN(v1.trending_date) effective_date
FROM videos v LEFT JOIN videos v1 ON v.client_video_id = v1.client_video_id 
WHERE 
v.client_video_id =v1.client_video_id 
AND
v.title <> v1.title
AND 
v.title <>'Deleted video'
AND 
v1.title <>'Deleted video'
GROUP BY v.client_video_id, v.title, v1.title) 
SELECT cte.old_title, cte.new_title, cte.effective_date
FROM cte JOIN dim_videos_view dv ON cte.client_video_id = dv.yt_video_id 
WHERE (cte.client_video_id, cte.effective_date) IN
(SELECT client_video_id, MAX(effective_date)
FROM cte
GROUP BY client_video_id)
