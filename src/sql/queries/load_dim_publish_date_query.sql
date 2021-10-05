INSERT INTO dim_publish_date (publish_date, week_of_the_year, quarter, day_of_the_week)
SELECT t.date,  
DATE_PART('week',t.date) AS week_of_the_year, 
EXTRACT(QUARTER FROM t.date) AS quarter,
CASE WHEN EXTRACT(DOW FROM t.date) = 0 THEN 'Sunday'
WHEN EXTRACT(DOW FROM t.date) = 1 THEN 'Monday'
WHEN EXTRACT(DOW FROM t.date) = 2 THEN 'Tuesday'
WHEN EXTRACT(DOW FROM t.date) = 3 THEN 'Wednesday'
WHEN EXTRACT(DOW FROM t.date) = 4 THEN 'Thursday'
WHEN EXTRACT(DOW FROM t.date) = 5 THEN 'Friday'
WHEN EXTRACT(DOW FROM t.date) = 6 THEN 'Saturday' END
AS day_of_the_week
FROM (SELECT DISTINCT publish_time::DATE AS date FROM videos) t;