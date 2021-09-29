INSERT INTO category(client_category_id, category, assignable)
SELECT 
category_id,
category,
CAST(assignable AS BOOLEAN)
FROM raw_category 
ON CONFLICT ON CONSTRAINT category_unique DO NOTHING;