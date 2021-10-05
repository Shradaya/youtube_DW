CREATE TABLE dim_publish_date(
date_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
publish_date DATE,
week_of_the_year INT,
quarter INT,
day_of_the_week VARCHAR(15)
);
