INSERT INTO dim_category (yt_category_id, category, assignable)
SELECT client_category_id, category, assignable FROM category;