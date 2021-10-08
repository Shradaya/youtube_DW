CREATE TABLE videos(
video_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
client_video_id VARCHAR(500) NOT NULL,
trending_date DATE NOT NULL,
title VARCHAR(15000) NOT NULL,
channel_title VARCHAR(15000) NOT NULL,
category_id VARCHAR(500) NOT NULL,
publish_time TIMESTAMP NOT NULL CONSTRAINT videos_publish_time CHECK (trending_date >= publish_time::DATE),
tags VARCHAR(15000),
views INT NOT NULL,
likes INT NOT NULL,
dislikes INT NOT NULL,
comment_count INT NOT NULL,
comments_disabled BOOLEAN NOT NULL,
ratings_disabled BOOLEAN NOT NULL,
video_error_or_removed BOOLEAN NOT NULL,
country VARCHAR(500) NOT NULL,
diff_publish_trend INT
);