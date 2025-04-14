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

# Customers

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

# Orders

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending','completed','canceled','shipped','returned') DEFAULT 'pending',
    total DECIMAL(10,2) DEFAULT 0,
    CONSTRAINT fk_orders_customer FOREGIN KEY (customer_id)
        REFERENCES customers(id)
        ON UPDATE CASCADE ON DELETE CASCADE
)

# Order Details

CREATE TABLE order_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_order_details_order FOREIGN KEY (order_id)
      REFERENCES orders(id)
      ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_order_details_product FOREIGN KEY (product_id)
      REFERENCES products(id)
      ON UPDATE CASCADE ON DELETE RESTRICT
) 
