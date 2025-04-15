-- Create categories table with additional fields
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Product Category ID',
    name VARCHAR(100) NOT NULL,
    description TEXT,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT = 'Product Category Information';

-- Create products table with additional fields
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    summary VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    description TEXT,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    category_id INT NOT NULL,
    CONSTRAINT fk_products_category FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create auth table
CREATE TABLE auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    phone_number VARCHAR(20),
    email VARCHAR(50),
    position VARCHAR(100),
    department VARCHAR(100),
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    auth_id INT NOT NULL UNIQUE,
    CONSTRAINT fk_users_auth FOREIGN KEY (auth_id)
        REFERENCES auth(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create customers table with updated fields
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    phone_number VARCHAR(20),
    email VARCHAR(50),
    address VARCHAR(100),
    auth_id INT NOT NULL UNIQUE,
    CONSTRAINT fk_customers_auth FOREIGN KEY (auth_id)
        REFERENCES auth(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create orders table with updated fields
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    user_id INT,
    status ENUM('ORDERED', 'SHIPPING', 'CANCELLED', 'COMPLETED') NOT NULL DEFAULT 'ORDERED',
    description TEXT,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create order_items table (replacing order_details)
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    description TEXT,
    delete_flg BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Insert sample data for categories
INSERT INTO categories (name, description, delete_flg) VALUES
('Electronics', 'Devices and gadgets', FALSE),
('Clothing', 'Apparel and accessories', FALSE),
('Books', 'Physical and digital books', FALSE),
('Home & Garden', 'Furniture and decor', FALSE),
('Toys', 'Games and playthings', FALSE);

-- Insert sample data for products
INSERT INTO products (name, summary, price, quantity, description, delete_flg, category_id) VALUES
('Smartphone X', 'Latest model with 128GB', 699.99, 50, 'High-performance smartphone', FALSE, 1),
('Wireless Earbuds', 'Noise-canceling', 129.99, 100, 'Bluetooth earbuds', FALSE, 1),
('Cotton T-Shirt', 'Casual wear', 19.99, 200, 'Comfortable t-shirt', FALSE, 2),
('Denim Jeans', 'Slim-fit', 49.99, 150, 'Blue jeans', FALSE, 2),
('Sci-Fi Novel', 'Space adventure', 14.99, 75, 'Bestselling book', FALSE, 3),
('Programming Guide', 'Learn Python', 29.99, 60, 'Python programming book', FALSE, 3),
('Table Lamp', 'LED desk lamp', 39.99, 40, 'Modern lamp', FALSE, 4),
('Throw Pillow', 'Decorative', 24.99, 80, 'Soft cushion', FALSE, 4),
('Board Game', 'Family fun', 34.99, 90, 'Strategy game', FALSE, 5),
('Action Figure', 'Superhero', 15.99, 120, 'Collectible figure', FALSE, 5);

-- Insert sample data for auth
INSERT INTO auth (username, password, is_admin, is_staff, is_active, delete_flg) VALUES
('john_doe', '$2b$12$hashedpassword1', FALSE, FALSE, TRUE, FALSE),
('jane_smith', '$2b$12$hashedpassword2', FALSE, FALSE, TRUE, FALSE),
('bob_jones', '$2b$12$hashedpassword3', FALSE, FALSE, TRUE, FALSE),
('alice_brown', '$2b$12$hashedpassword4', TRUE, FALSE, TRUE, FALSE),
('charlie_wilson', '$2b$12$hashedpassword5', FALSE, TRUE, TRUE, FALSE);

-- Insert sample data for users
INSERT INTO users (last_name, first_name, phone_number, email, position, department, delete_flg, auth_id) VALUES
('Doe', 'John', '555-0101', 'john@example.com', 'Developer', 'IT', FALSE, 1),
('Brown', 'Alice', '555-0104', 'alice@example.com', 'Manager', 'Admin', FALSE, 4),
('Wilson', 'Charlie', '555-0105', 'charlie@example.com', 'Analyst', 'Data', FALSE, 5);

-- Insert sample data for customers
INSERT INTO customers (last_name, first_name, phone_number, email, address, auth_id) VALUES
('Smith', 'Jane', '555-0102', 'jane@example.com', '123 Main St, City', 2),
('Jones', 'Bob', '555-0103', 'bob@example.com', '456 Oak Ave, Town', 3);

-- Insert sample data for orders
INSERT INTO orders (order_number, customer_id, user_id, status, description, delete_flg) VALUES
('ORD001', 1, NULL, 'COMPLETED', 'Order for electronics', FALSE),
('ORD002', 2, 1, 'ORDERED', 'Clothing order', FALSE),
('ORD003', 1, 2, 'SHIPPING', 'Books order', FALSE),
('ORD004', 2, 3, 'COMPLETED', 'Home decor order', FALSE),
('ORD005', 1, NULL, 'CANCELLED', 'Toys order', FALSE);

-- Insert sample data for order_items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, description, delete_flg) VALUES
(1, 1, 1, 699.99, 'Smartphone X', FALSE),
(1, 2, 1, 129.99, 'Wireless Earbuds', FALSE),
(2, 3, 2, 19.99, 'Cotton T-Shirt', FALSE),
(2, 4, 1, 49.99, 'Denim Jeans', FALSE),
(3, 5, 1, 14.99, 'Sci-Fi Novel', FALSE),
(3, 6, 1, 29.99, 'Programming Guide', FALSE),
(4, 7, 1, 39.99, 'Table Lamp', FALSE),
(4, 8, 1, 24.99, 'Throw Pillow', FALSE),
(5, 9, 1, 34.99, 'Board Game', FALSE);