# Categories

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

# Products

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Define foreign key to categories
    CONSTRAINT fk_products_category FOREGIN KEY (category_id)
        REFERENCES categories(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
)
    -- The foreign key uses CASCADE on updates (if a category’s ID were to be changed) and RESTRICT 
    -- on delete to prevent accidental deletions of a category that still has products.f