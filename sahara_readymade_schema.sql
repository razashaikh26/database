-- Create the database
CREATE DATABASE IF NOT EXISTS SaharaReadymade;
USE SaharaReadymade;

-- Create Categories table
CREATE TABLE IF NOT EXISTS Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Products table
CREATE TABLE IF NOT EXISTS Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- Create Customers table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Orders table
CREATE TABLE IF NOT EXISTS Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) DEFAULT 0.00,
    status ENUM('pending', 'processing', 'completed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Create OrderDetails table
CREATE TABLE IF NOT EXISTS OrderDetails (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_time DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Create Users table for authentication
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (username: razashaikh, password: jauwwad)
INSERT INTO Users (username, password_hash, full_name) 
VALUES ('razashaikh', 'jauwwad', 'Raza Shaikh');

-- Insert sample categories
INSERT INTO Categories (category_name, description) VALUES
('Men''s Clothing', 'Clothing items for men'),
('Women''s Clothing', 'Clothing items for women'),
('Children''s Clothing', 'Clothing items for children'),
('Accessories', 'Various clothing accessories');

-- Insert sample products
INSERT INTO Products (product_name, category_id, price, stock_quantity) VALUES
('Men''s T-Shirt', 1, 599.99, 50),
('Women''s Dress', 2, 1299.99, 30),
('Kids Jeans', 3, 499.99, 25),
('Scarf', 4, 299.99, 100),
('Men''s Jeans', 1, 899.99, 40),
('Women''s Top', 2, 699.99, 35);

-- Insert sample customers
INSERT INTO Customers (first_name, last_name, phone_number, email, address) VALUES
('John', 'Doe', '9876543210', 'john@example.com', '123 Main St, Mumbai'),
('Jane', 'Smith', '8765432109', 'jane@example.com', '456 Park Ave, Delhi'),
('Amit', 'Patel', '7654321098', 'amit@example.com', '789 Lake Rd, Bangalore');

-- Insert sample orders
INSERT INTO Orders (customer_id, total_amount, status) VALUES
(1, 1199.98, 'completed'),
(2, 1299.99, 'processing'),
(3, 799.98, 'pending');

-- Insert sample order details
INSERT INTO OrderDetails (order_id, product_id, quantity, price_at_time) VALUES
(1, 1, 2, 599.99),
(2, 2, 1, 1299.99),
(3, 4, 1, 299.99),
(3, 5, 1, 499.99); 