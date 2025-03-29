CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    cost INT NOT NULL,
    percent_recycled INT,
    category VARCHAR(255),
    materials TEXT,
    store_picture_url TEXT,
    product_picture_url TEXT
);

CREATE TABLE machines (
    id SERIAL PRIMARY KEY,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL
);