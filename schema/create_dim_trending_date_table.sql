CREATE TABLE dim_trending_date(
date_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
trending_date DATE,
week_of_the_year INT,
quarter INT,
day_of_the_week VARCHAR(15)
);
