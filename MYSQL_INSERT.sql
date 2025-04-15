-- Insert sample data for categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Devices and gadgets'),
('Clothing', 'Apparel and accessories'),
('Books', 'Physical and digital books'),
('Home & Garden', 'Furniture and decor'),
('Toys', 'Games and playthings');

-- Insert sample data for products
INSERT INTO products (category_id, name, description, price, stock) VALUES
(1, 'Smartphone X', 'Latest model with 128GB storage', 699.99, 50),
(1, 'Wireless Earbuds', 'Noise-canceling earbuds', 129.99, 100),
(2, 'Cotton T-Shirt', 'Comfortable casual wear', 19.99, 200),
(2, 'Denim Jeans', 'Slim-fit blue jeans', 49.99, 150),
(3, 'Sci-Fi Novel', 'Bestselling space adventure', 14.99, 75),
(3, 'Programming Guide', 'Learn Python programming', 29.99, 60),
(4, 'Table Lamp', 'Modern LED desk lamp', 39.99, 40),
(4, 'Throw Pillow', 'Decorative cushion', 24.99, 80),
(5, 'Board Game', 'Family strategy game', 34.99, 90),
(5, 'Action Figure', 'Collectible superhero figure', 15.99, 120);

-- Insert sample data for customers
INSERT INTO customers (username, email, hashed_password, first_name, last_name) VALUES
('john_doe', 'john@example.com', '$2b$12$hashedpassword1', 'John', 'Doe'),
('jane_smith', 'jane@example.com', '$2b$12$hashedpassword2', 'Jane', 'Smith'),
('bob_jones', 'bob@example.com', '$2b$12$hashedpassword3', 'Bob', 'Jones'),
('alice_brown', 'alice@example.com', '$2b$12$hashedpassword4', 'Alice', 'Brown'),
('charlie_wilson', 'charlie@example.com', '$2b$12$hashedpassword5', 'Charlie', 'Wilson');

-- Insert sample data for orders
INSERT INTO orders (customer_id, order_date, status, total) VALUES
(1, '2025-04-10 10:30:00', 'completed', 749.98),
(2, '2025-04-11 14:15:00', 'pending', 149.98),
(3, '2025-04-12 09:00:00', 'shipped', 64.98),
(4, '2025-04-13 16:45:00', 'completed', 44.98),
(5, '2025-04-14 11:20:00', 'canceled', 0.00);

-- Insert sample data for order_details
INSERT INTO order_details (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 699.99),  -- Smartphone X
(1, 3, 1, 49.99),   -- Denim Jeans
(2, 2, 1, 129.99),  -- Wireless Earbuds
(2, 4, 1, 19.99),   -- Cotton T-Shirt
(3, 5, 1, 14.99),   -- Sci-Fi Novel
(3, 6, 1, 49.99),   -- Programming Guide
(4, 7, 1, 24.99),   -- Throw Pillow
(4, 8, 1, 19.99),   -- Cotton T-Shirt
(5, 9, 1, 34.99);   -- Board Game