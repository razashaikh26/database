import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_database():
    """Initialize the database with required schema if not already set up"""
    
    host = os.environ.get("DB_HOST", "localhost")
    user = os.environ.get("DB_USER", "root")
    password = os.environ.get("DB_PASSWORD", "")
    database = os.environ.get("DB_NAME", "SaharaReadymade")
    
    # First connect without specifying database to create it if needed
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        conn.commit()
        
        # Close connection
        cursor.close()
        conn.close()
        
        # Reconnect with database specified
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL,
            description TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            category_id INT,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INT DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            phone_number VARCHAR(15),
            email VARCHAR(100),
            address TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10, 2) DEFAULT 0,
            status VARCHAR(20) DEFAULT 'Processing',
            payment_status VARCHAR(20) DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OrderDetails (
            detail_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            product_id INT,
            quantity INT NOT NULL,
            price_at_time DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        )
        """)
        
        conn.commit()
        print("Database initialization completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    initialize_database() 