CREATE TABLE dim_videos(
video_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
yt_video_id VARCHAR(500),
category_id INT,
channel_id INT,
date_id INT,
video_title VARCHAR(1000),
publish_time TIMESTAMP,
ratings_disabled BOOLEAN,
cmt_disabled BOOLEAN,
video_error_or_removed BOOLEAN,
CONSTRAINT fk_dv_category_id FOREIGN KEY (category_id) REFERENCES dim_category(category_id),
CONSTRAINT fk_dv_channel_id FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id),
CONSTRAINT fk_dv_date_id FOREIGN KEY (date_id) REFERENCES dim_publish_date(date_id)
);