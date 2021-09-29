CREATE TABLE category(
category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
client_category_id VARCHAR(255),
category VARCHAR(255),
assignable BOOLEAN,
CONSTRAINT category_unique UNIQUE (client_category_id, category, assignable)
);