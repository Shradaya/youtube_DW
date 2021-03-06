 ## The file structure of this repo:
```
data/             # Folder containing the datasets in different formats.
  *.csv
  *.json
 docs/           # Folder containing .md files for assignment.      
   *.md
   *.png
schema/          # Folder containing different DDL sql queries.
  *.sql    
src/
  pipeline/      # Folder containing python scripts    
    .env
    *.py
  sql/
    queries/     # Folder containing sql DML queries
      *.sql
```
## 1. Schema defined by the sql in Schema directory


* `Schema/create_raw_category_table.sql` file:
``` 
CREATE TABLE raw_category(
  kind VARCHAR(1000),
  etag VARCHAR(1000),
  category_id VARCHAR(1000),
  channel_id VARCHAR(1000),
  category VARCHAR(1000),
  assignable VARCHAR(1000),
  country VARCHAR(1000)
);
```
Here I created a table `raw_category` with necessary columns from dataset in the given json file.

The dataset has multiple category files regarding each different countries. However, the fields used are same so, we will be using a single raw table to store all the data. 
I have added an additional column in order to know which country does the category come from.

All entities are declared `VARCHAR(500)` because, for a bulk datas to extract, we may not delare exact datatypes which may cause problems later.
For example: Format for date `2021-12-12` can come as `12-12-2021` and thus declaring datatypes may cause problem later.

* `schema/create_raw_videos_table.sql` file:
```
CREATE TABLE raw_videos(
  video_id VARCHAR(500),
  trending_date VARCHAR(500),
  title VARCHAR(500),
  channel_title VARCHAR(500),
  category_id VARCHAR(500),
  publish_time VARCHAR(500),
  tags VARCHAR(500),
  views VARCHAR(500),
  likes VARCHAR(500),
  dislikes VARCHAR(500),
  comment_count VARCHAR(500),
  thumbnail_link VARCHAR(500),
  comments_disabled VARCHAR(500),
  ratings_disabled VARCHAR(500),
  video_error_or_removed VARCHAR(500),
  description VARCHAR(500),
  country VARCHAR(500)
);
```
This is SQL file to create `raw_videos` table according to dataset in csv file.

* `Schema/create_raw_category_archive_table.sql` file:
``` 
CREATE TABLE raw_category_archive(
  kind VARCHAR(1000),
  etag VARCHAR(1000),
  category_id VARCHAR(1000),
  channel_id VARCHAR(1000),
  category VARCHAR(1000),
  assignable VARCHAR(1000),
  file_name VARCHAR(1000)
);
```
I created a table `raw_category_archive` with necessary columns for data in given json file and an additional column to denote the file from which the data has been taken.


* `schema/create_raw_videos_archive_table.sql` file:
```
CREATE TABLE raw_videos_archive(
  video_id VARCHAR(500),
  trending_date VARCHAR(500),
  title VARCHAR(500),
  channel_title VARCHAR(500),
  category_id VARCHAR(500),
  publish_time VARCHAR(500),
  tags VARCHAR(500),
  views VARCHAR(500),
  likes VARCHAR(500),
  dislikes VARCHAR(500),
  comment_count VARCHAR(500),
  thumbnail_link VARCHAR(500),
  comments_disabled VARCHAR(500),
  ratings_disabled VARCHAR(500),
  video_error_or_removed VARCHAR(500),
  description VARCHAR(500),
  file_name VARCHAR(500)
);
```

I created a table `raw_videos_archive` with necessary columns from dataset in data with a column for file_name in order to keep track of the source file. This file stores all the necessary data persistently.

* `schema/create_category_table.sql` file:
```
CREATE TABLE category(
  category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  client_category_id VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  assignable BOOLEAN NOT NULL,
  CONSTRAINT category_unique UNIQUE (client_category_id, category, assignable)
);
```

I have created a table named category in order to store the necessary category data for the analysis and also provide them with the respective data types. 
With a little digging it was found that the category_id, category and assignable are the important datas. The other values aren't as necessary. Also, though the files were divided into multiple json files it had similar datasets with few categories missing in a few files. So, for the category data I have decided to use only the categories without separating them using countries.
For this purpose I have defined a CONSTRAINT, category_unique which allows only the unique combination of (client_category_id, category, assignable) to be in the table

* `schema/create_videos_table.sql` file:
```
CREATE TABLE videos(
  video_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  client_video_id VARCHAR(500) NOT NULL,
  trending_date DATE NOT NULL,
  title VARCHAR(15000) NOT NULL,
  channel_title VARCHAR(15000) NOT NULL,
  category_id VARCHAR(500) NOT NULL,
  publish_time TIMESTAMP NOT NULL 
  CONSTRAINT videos_publish_time CHECK (trending_date >= publish_time::DATE),
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
```

I have created a table called videos to import the necessary data and provide them a specific data type.
I have added few additional colums for numercal values like diff_publish_first_trend to calculate difference between the publish and trending date.


* `schema/create_dim_category_table.sql` file:
```
CREATE TABLE dim_category(
  category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  yt_category_id VARCHAR(500),
  category VARCHAR(500),
  assignable BOOLEAN
);
```

It is the first dimension table that I have created. This table holds the different category of video that were on the trending list.

* `schema/create_dim_channel_table.sql` file:
```
CREATE TABLE dim_channel(
  channel_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  channel_name VARCHAR(500)
);
```
This is a dimension table which holds the distinct channels that are available in the youtube trending.

* `schema/create_dim_country_table.sql` file:
```
CREATE TABLE dim_country(
  country_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  country_name VARCHAR(50)
);
```
For this project we have 10 different countries. This table is used to store the name of the different countries.

* `schema/create_dim_publish_date_table.sql` file:
```
CREATE TABLE dim_publish_date(
  date_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  publish_date DATE,
  week_of_the_year INT,
  quarter INT,
  day_of_the_week VARCHAR(15)
);
```
It is the dimension table used to categorize the published date.

* `schema/create_dim_trending_date_table.sql` file:
```
CREATE TABLE dim_trending_date(
  date_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  trending_date DATE,
  week_of_the_year INT,
  quarter INT,
  day_of_the_week VARCHAR(15)
);
```
It is the dimension table used to categorize the trending date.


* `schema/create_dim_videos_table.sql` file:
```
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
  tags VARCHAR(1500),
  old_title VARCHAR(1500) DEFAULT NULL, 
  effective_date DATE DEFAULT NULL,
  CONSTRAINT fk_dv_category_id FOREIGN KEY (category_id) 
  REFERENCES dim_category(category_id) ON DELETE CASCADE,
  CONSTRAINT fk_dv_channel_id FOREIGN KEY (channel_id) 
  REFERENCES dim_channel(channel_id) ON DELETE CASCADE,
  CONSTRAINT fk_dv_date_id FOREIGN KEY (date_id) 
  REFERENCES dim_publish_date(date_id) ON DELETE CASCADE,
  CONSTRAINT unique_yt_video_id UNIQUE(yt_video_id)
);
```
This table is used to store the informations regarding the video. 

* `schema/create_fact_trend_video_table.sql` file:
```
CREATE TABLE fact_video_trend(
  video_trend_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  video_id INT,
  country_id INT,
  date_id INT,
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
```
This table is used to store the information of the videos with regards to the different trending date. The values from this table can be used for analysis.

* `schema/create_dim_videos_view.sql` file:
```
CREATE VIEW dim_videos_view 
  (yt_video_id, category_id, channel_id, date_id, video_title, publish_time,
  ratings_disabled, cmt_disabled, video_error_or_removed, tags) AS
  SELECT 
  v.client_video_id, 
  dc.category_id,
  dch.channel_id,
  dd.date_id,
  v.title,
  FROM videos v 
  JOIN dim_category dc ON v.category_id = dc.yt_category_id
  JOIN dim_channel dch ON v.channel_title = dch.channel_name
  JOIN dim_publish_date dd ON v.publish_time::date = dd.publish_date
  WHERE v.video_id IN
  (SELECT video_id FROM videos 
  WHERE (client_video_id, trending_date)  IN
  (SELECT client_video_id, MAX(trending_date) FROM
  videos
  GROUP BY client_video_id));
```
Here, I have created a view in order to assist in creation of list of videos with title change.


* `schema/video_title_change.sql` file:

```
CREATE TABLE video_title_change(
  yt_video_id VARCHAR(1000),
  old_title VARCHAR(1000),
  new_title VARCHAR(1000),
  effective_date DATE
);
```
## 2. `connectdb.py` file in  src/pipeline/.
We connect to Postgresql database regularly in each script through `psycopg2` so it made sense to create a separate file for the repeating function. I have used environment variables to get around revealing srcret informations.

* `connectdb.py` file:
```
import os
from dotenv import load_dotenv
load_dotenv()

def connect(psy):
    return psy.connect(
        host = os.getenv('host'),
        database = os.getenv('db1'),
        user = os.getenv('user'),
        password = os.getenv('password'),
        port = os.getenv('port')
    )
```


## 3. `query.py` file in src/pipeline/.
This file is used to store the file path of the DML sql queries in use.

* `query.py` file:

```
extract_raw_category_data_query = '../sql/queries/extract_raw_category_data_query.sql'
extract_raw_category_archive_data_query = '../sql/queries/extract_raw_category_archive_data_query.sql'

extract_raw_videos_data_query = '../sql/queries/extract_raw_videos_data_query.sql'
extract_raw_videos_archive_data_query = '../sql/queries/extract_raw_videos_archive_data_query.sql'

extract_category_data_from_raw_query = '../sql/queries/extract_category_data_from_raw_query.sql'
extract_video_data_from_raw_query = '../sql/queries/extract_video_data_from_raw_query.sql'

load_dim_category_query = '../sql/queries/load_dim_category_query.sql'
load_dim_channel_query = '../sql/queries/load_dim_channel_query.sql'
load_dim_country_query = '../sql/queries/load_dim_country_query.sql'
load_dim_publish_date_query = '../sql/queries/load_dim_publish_date_query.sql'
load_dim_trending_date_query = '../sql/queries/load_dim_trending_date_query.sql'
load_dim_videos_query = '../sql/queries/load_dim_videos_query.sql'
load_fact_video_trend_query = '../sql/queries/load_fact_video_trend_query.sql'
load_videos_with_title_change_query = '../sql/queries/load_videos_with_title_change.sql'
```


## 4. `sql.py` file in src/pipeline/.
In this project we are reading queries multiple times from sql files so a separate function to read the file has been defined in this file.

* `sql.py` file:
```
def query(filepath):
    with open(filepath, 'r') as file:
        sql_query = "".join(file.readlines())
    return sql_query
```

## 5. `.env` file in src/pipeline/.

This file is used to define the environment variables which are to be kept a srcret. This file is included in gitignore.

## 6. `extract_raw_category_data_query.sql` file in src/sql/queries/.

It is a DML query to insert data into the raw_category table

* `extract_raw_category_data_query.sql` file:
```
INSERT INTO raw_category
(kind, etag, category_id, channel_id, category, assignable, country)
VALUES (%s, %s, %s, %s, %s, %s, %s);

```

## 7. `extract_raw_videos_data_query.sql` file in src/sql/queries/.

It is a DML query to insert data into the raw_videos table

* `extract_raw_videos_data_query.sql` file:
```
INSERT INTO raw_videos(
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
country    
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
```

## 8. `extract_raw_category_archive_data_query.sql` file in src/sql/queries/.

It is a DML query to insert data into the raw_product table

* `extract_raw_category_archive_data_query.sql` file:
```
INSERT INTO raw_category_archive
(kind, etag, category_id, channel_id, category, assignable, file_name)
VALUES (%s, %s, %s, %s, %s, %s, %s);
```


## 9. `extract_raw_videos_archive_data_query.sql` file in src/sql/queries/.

It is a DML query to insert data into the raw_videos_archive table.

* `extract_raw_videos_archive_data_query.sql` file:
```
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
```

## 10. `extract_category_data_from_raw_query.sql` file in src/sql/queries

It is a DML query to insert data into the category table from the raw datas stored in the raw_category table. Here the category_unique constraint is used to identify only the unqiue category regarding the id, category and assignable.

* `extract_category_data_from_raw_query.sql` file:
```
INSERT INTO category(client_category_id, category, assignable)
SELECT 
category_id,
category,
CAST(assignable AS BOOLEAN)
FROM raw_category 
ON CONFLICT ON CONSTRAINT category_unique DO NOTHING;
```


## 11. `extract_video_data_from_raw_query.sql` file in src/sql/queries

It is a DML query to insert data into the video table from the raw datas stored in the raw tables.
Here, we have cast the data variables on to the variables as per need, while also adding two fields, diff_publish_trend and ratio_like_dislike. The trending date's format has also been converted to a viable one.

* `extract_video_data_from_raw_query.sql` file:
```
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
  FROM raw_videos WHERE video_id <> '#NAME?'
  OR video <> '#VALUE!';
```

## 12. `load_dim_category_query.sql` file in src/sql/queries

It is a DML query to insert data into the dim_category table from the cateogory table formed from the transformation of data from the raw_category table.

* `load_dim_category_query.sql` file:
```
INSERT INTO dim_category (yt_category_id, category, assignable)
SELECT client_category_id, category, assignable FROM category;
```

## 13. `load_dim_channel_query.sql` file in src/sql/queries

It is a DML query to insert data into the dim_channel table.

* `load_dim_channel_query.sql` file:
```
INSERT INTO dim_channel(channel_name)
SELECT DISTINCT channel_title FROM videos;
```


## 14. `load_dim_country_query.sql` file in src/sql/queries

It is a DML query to insert data into the dim_country table.

* `load_dim_country_query.sql` file:
```
INSERT INTO dim_country(country_name)
SELECT DISTINCT country FROM videos;
```

## 15. `load_dim_publish_date_query.sql` file in src/sql/queries

It is a DML query to insert data into the dim_publish_date table.

* `load_dim_publish_date_query.sql` file:
```
INSERT INTO dim_publish_date (full_date, week_of_the_year, quarter, year, month, date, day_of_the_week)
SELECT t.date,  
DATE_PART('week',t.date) AS week_of_the_year, 
EXTRACT(QUARTER FROM t.date) AS quarter,
EXTRACT(YEAR FROM t.date) AS year,
EXTRACT(MONTH FROM t.date) AS month,
EXTRACT(DAY FROM t.date) AS date,
CASE WHEN EXTRACT(DOW FROM t.date) = 0 THEN 'Sunday'
WHEN EXTRACT(DOW FROM t.date) = 1 THEN 'Monday'
WHEN EXTRACT(DOW FROM t.date) = 2 THEN 'Tuesday'
WHEN EXTRACT(DOW FROM t.date) = 3 THEN 'Wednesday'
WHEN EXTRACT(DOW FROM t.date) = 4 THEN 'Thursday'
WHEN EXTRACT(DOW FROM t.date) = 5 THEN 'Friday'
WHEN EXTRACT(DOW FROM t.date) = 6 THEN 'Saturday' END
AS day_of_the_week
FROM (SELECT DISTINCT publish_time::DATE AS date FROM videos) t;
```


## 16. `load_dim_trending_date_query.sql` file in src/sql/queries

It is a DML query to insert data into the dim_trending_date table.

* `load_dim_trending_date_query.sql` file:
```
INSERT INTO dim_trending_date (full_date, week_of_the_year, quarter, year, month, date, day_of_the_week)
SELECT t.date,  
DATE_PART('week',t.date) AS week_of_the_year, 
EXTRACT(QUARTER FROM t.date) AS quarter,
EXTRACT(YEAR FROM t.date) AS year,
EXTRACT(MONTH FROM t.date) AS month,
EXTRACT(DAY FROM t.date) AS date,
CASE WHEN EXTRACT(DOW FROM t.date) = 0 THEN 'Sunday'
WHEN EXTRACT(DOW FROM t.date) = 1 THEN 'Monday'
WHEN EXTRACT(DOW FROM t.date) = 2 THEN 'Tuesday'
WHEN EXTRACT(DOW FROM t.date) = 3 THEN 'Wednesday'
WHEN EXTRACT(DOW FROM t.date) = 4 THEN 'Thursday'
WHEN EXTRACT(DOW FROM t.date) = 5 THEN 'Friday'
WHEN EXTRACT(DOW FROM t.date) = 6 THEN 'Saturday' END
AS day_of_the_week
FROM (SELECT DISTINCT trending_date AS date FROM videos) t;
```


## 17. `load_dim_videos_query.sql` file in src/sql/queries

It is a DML query to insert data into the dim_videos table.

* `load_dim_videos_query.sql` file:
```
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
LEFT JOIN video_title_change vtc ON vtc.new_title = v.title 
WHERE v.video_id IN
(SELECT video_id FROM videos 
WHERE (client_video_id, trending_date)  IN
(SELECT client_video_id, MAX(trending_date) FROM
videos GROUP BY client_video_id))
ON CONFLICT ON CONSTRAINT unique_yt_video_id DO NOTHING;
```

## 18. `load_videos_with_title_change.sql` file in src/sql/queries

It is a DML query to load videos with title change.

* `load_videos_with_title_change.sql` file:

```
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
```
## 19. `load_fact_video_trend_query.sql` file in src/sql/queries

It is a DML query to insert data into the fact_video_trend table.

* `load_fact_video_trend_query.sql` file:

```
INSERT INTO fact_video_trend (video_id, country_id, date_id, views, likes, dislike, cmt_count,
							 diff_publish_trend, before_after_flag)
SELECT 
dv.video_id,
dc.country_id,
dd.date_id,
v."views",
v.likes,
v.dislikes,
v.comment_count,
v.diff_publish_trend,
CASE WHEN dv.effective_date <= v.trending_date THEN 1
     WHEN dv.effective_date > v.trending_date THEN 0
     ELSE null
     END AS before_after_flag
FROM videos v
JOIN dim_country dc ON v.country = dc.country_name 
JOIN dim_videos dv ON dv.yt_video_id = v.client_video_id 
JOIN dim_trending_date dd ON dd.trending_date = v.trending_date 
```