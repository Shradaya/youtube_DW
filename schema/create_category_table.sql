CREATE TABLE category(
category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
client_category_id VARCHAR(255) NOT NULL,
category VARCHAR(255) NOT NULL,
assignable BOOLEAN NOT NULL,
CONSTRAINT category_unique UNIQUE (client_category_id, category, assignable)
);