CREATE TABLE fact_video_trend(
video_trend_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
video_id INT,
country_id INT,
date_id INT,
trending_date DATE,
views INT,
likes INT,
dislike INT,
cmt_count INT,
diff_publish_trend INT,
CONSTRAINT fk_fvt_video_id FOREIGN KEY (video_id) 
REFERENCES dim_videos(video_id) ON DELETE CASCADE,
CONSTRAINT fk_fvt_country_id FOREIGN KEY (country_id) 
REFERENCES dim_country(country_id) ON DELETE CASCADE,
CONSTRAINT fk_fvt_date_id FOREIGN KEY (date_id) 
REFERENCES dim_trending_date(date_id) ON DELETE CASCADE
);