INSERT INTO raw_videos_archive(
video_id,
trending_date,
title,
channel_title,
category_id,
publish_time,
tags,
views,
likes,
dislikes,
comment_count,
thumbnail_link,
comments_disabled,
ratings_disabled,
video_error_or_removed,
description,
file_name
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)