CREATE TABLE dim_category(
category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
yt_category_id VARCHAR(500),
category VARCHAR(500),
assignable BOOLEAN
);