-- Sample data for SaharaReadymade database
USE SaharaReadymade;

-- Insert sample categories
INSERT INTO Categories (category_name, description) 
VALUES 
('Men\'s Clothing', 'Clothing items for men'),
('Women\'s Clothing', 'Clothing items for women'),
('Kids\' Clothing', 'Clothing items for children'),
('Accessories', 'Various accessories');

-- Insert sample products
INSERT INTO Products (product_name, category_id, price, stock_quantity)
VALUES
('Men\'s T-Shirt', 1, 599.99, 50),
('Women\'s Dress', 2, 1299.99, 30),
('Kids\' Jeans', 3, 499.99, 25),
('Scarf', 4, 299.99, 40),
('Men\'s Formal Shirt', 1, 899.99, 35),
('Women\'s Blouse', 2, 799.99, 45);

-- Insert sample customers
INSERT INTO Customers (first_name, last_name, phone_number, email, address)
VALUES
('John', 'Doe', '9876543210', 'john.doe@example.com', '123 Main St, Mumbai'),
('Jane', 'Smith', '8765432109', 'jane.smith@example.com', '456 Park Ave, Delhi'),
('Raj', 'Kumar', '7654321098', 'raj.kumar@example.com', '789 Lake View, Bangalore');

-- Sample orders
INSERT INTO Orders (customer_id, total_amount, status, payment_status)
VALUES
(1, 1199.98, 'Delivered', 'Paid'),
(2, 1299.99, 'Processing', 'Pending'),
(3, 899.99, 'Shipped', 'Paid');

-- Sample order details
INSERT INTO OrderDetails (order_id, product_id, quantity, price_at_time)
VALUES
(1, 1, 2, 599.99),
(2, 2, 1, 1299.99),
(3, 5, 1, 899.99); 