INSERT INTO dim_country(country_name)
SELECT DISTINCT country FROM videos;