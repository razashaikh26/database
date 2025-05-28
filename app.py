from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import pandas as pd
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection class
class SaharaReadymadeDB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Razashaikh@12",
                database="SaharaReadymade"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Database Connection Error: {err}")
            raise

    def fetch_data(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching data: {err}")
            return []

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(f"Error executing query: {err}")
            return False

    def close(self):
        self.cursor.close()
        self.conn.close()

# Routes
@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # For demo purposes - replace with actual authentication
        if username == 'razashaikh' and password == 'jauwwad':
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

# Categories routes
@app.route('/categories')
def categories():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    categories = db.fetch_data("SELECT * FROM Categories")
    db.close()
    
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['POST'])
def add_category():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    category_name = request.form.get('category_name')
    description = request.form.get('description')
    
    if category_name:
        db = SaharaReadymadeDB()
        query = "INSERT INTO Categories (category_name, description) VALUES (%s, %s)"
        success = db.execute_query(query, (category_name, description))
        db.close()
        
        if success:
            flash('Category added successfully!', 'success')
        else:
            flash('Failed to add category!', 'danger')
    else:
        flash('Category name is required!', 'warning')
    
    return redirect(url_for('categories'))

# Products routes
@app.route('/products')
def products():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    products = db.fetch_data("""
        SELECT p.*, c.category_name 
        FROM Products p
        JOIN Categories c ON p.category_id = c.category_id
    """)
    categories = db.fetch_data("SELECT * FROM Categories")
    db.close()
    
    return render_template('products.html', products=products, categories=categories)

@app.route('/products/add', methods=['POST'])
def add_product():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    product_name = request.form.get('product_name')
    category_id = request.form.get('category_id')
    price = request.form.get('price')
    stock_quantity = request.form.get('stock_quantity')
    
    if product_name and category_id:
        db = SaharaReadymadeDB()
        query = """
        INSERT INTO Products (product_name, category_id, price, stock_quantity) 
        VALUES (%s, %s, %s, %s)
        """
        success = db.execute_query(query, (product_name, category_id, price, stock_quantity))
        db.close()
        
        if success:
            flash('Product added successfully!', 'success')
        else:
            flash('Failed to add product!', 'danger')
    else:
        flash('Product name and category are required!', 'warning')
    
    return redirect(url_for('products'))



# Customers routes
@app.route('/customers')
def customers():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    customers = db.fetch_data("SELECT * FROM Customers")
    db.close()
    
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['POST'])
def add_customer():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    address = request.form.get('address')
    
    if first_name and last_name:
        db = SaharaReadymadeDB()
        query = """
        INSERT INTO Customers (first_name, last_name, phone_number, email, address) 
        VALUES (%s, %s, %s, %s, %s)
        """
        success = db.execute_query(query, (first_name, last_name, phone_number, email, address))
        db.close()
        
        if success:
            flash('Customer added successfully!', 'success')
        else:
            flash('Failed to add customer!', 'danger')
    else:
        flash('First name and last name are required!', 'warning')
    
    return redirect(url_for('customers'))

# Orders routes
@app.route('/orders')
def orders():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    orders = db.fetch_data("""
    SELECT o.order_id, 
           CONCAT(c.first_name, ' ', c.last_name) as customer_name, 
           o.order_date, 
           o.total_amount, 
           o.status
    FROM Orders o
    JOIN Customers c ON o.customer_id = c.customer_id
    ORDER BY o.order_date DESC
    """)
    db.close()
    
    return render_template('orders.html', orders=orders)

@app.route('/orders/details/<int:order_id>')
def order_details(order_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    order = db.fetch_data("SELECT * FROM Orders WHERE order_id = %s", (order_id,))[0]
    customer = db.fetch_data("SELECT * FROM Customers WHERE customer_id = %s", (order['customer_id'],))[0]
    
    order_details = db.fetch_data("""
    SELECT p.product_name, od.quantity, od.price_at_time, 
           (od.quantity * od.price_at_time) as subtotal
    FROM OrderDetails od
    JOIN Products p ON od.product_id = p.product_id
    WHERE od.order_id = %s
    """, (order_id,))
    db.close()
    
    return render_template('order_details.html', order=order, customer=customer, order_details=order_details)

@app.route('/orders/update_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    new_status = request.form.get('status')
    
    db = SaharaReadymadeDB()
    success = db.execute_query("UPDATE Orders SET status = %s WHERE order_id = %s", (new_status, order_id))
    db.close()
    
    if success:
        flash(f'Order status updated to {new_status}!', 'success')
    else:
        flash('Failed to update order status!', 'danger')
    
    return redirect(url_for('order_details', order_id=order_id))

@app.route('/create_order')
def create_order_form():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    customers = db.fetch_data("SELECT customer_id, first_name, last_name FROM Customers")
    products = db.fetch_data("SELECT product_id, product_name, price, stock_quantity FROM Products WHERE stock_quantity > 0")
    db.close()
    
    return render_template('create_order.html', customers=customers, products=products)

@app.route('/create_order', methods=['POST'])
def create_order():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    customer_id = request.form.get('customer_id')
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))
    
    db = SaharaReadymadeDB()
    
    try:
        # Get product details first
        product = db.fetch_data("SELECT * FROM Products WHERE product_id = %s", (product_id,))[0]
        
        # Check if enough stock
        if product['stock_quantity'] < quantity:
            flash('Not enough stock available!', 'danger')
            db.close()
            return redirect(url_for('create_order_form'))
        
        # Create Order
        db.cursor.execute("INSERT INTO Orders (customer_id) VALUES (%s)", (customer_id,))
        order_id = db.cursor.lastrowid
        
        # Insert Order Details
        db.cursor.execute(
            "INSERT INTO OrderDetails (order_id, product_id, quantity, price_at_time) VALUES (%s, %s, %s, %s)",
            (order_id, product_id, quantity, product['price'])
        )
        
        # Update Total Amount
        total_amount = quantity * product['price']
        db.cursor.execute(
            "UPDATE Orders SET total_amount = %s WHERE order_id = %s", 
            (total_amount, order_id)
        )
        
        # Reduce Product Stock
        db.cursor.execute(
            "UPDATE Products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
            (quantity, product_id)
        )
        
        # Commit transaction
        db.conn.commit()
        flash(f'Order created successfully! Order ID: {order_id}', 'success')
        
    except mysql.connector.Error as err:
        # Rollback in case of error
        db.conn.rollback()
        flash(f'Error creating order: {err}', 'danger')
    finally:
        db.close()
    
    return redirect(url_for('orders'))

# Add these new routes after their respective sections

@app.route('/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    success = db.execute_query("DELETE FROM Categories WHERE category_id = %s", (category_id,))
    db.close()
    
    if success:
        flash('Category deleted successfully!', 'success')
    else:
        flash('Failed to delete category!', 'danger')
    
    return redirect(url_for('categories'))

@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    success = db.execute_query("DELETE FROM Products WHERE product_id = %s", (product_id,))
    db.close()
    
    if success:
        flash('Product deleted successfully!', 'success')
    else:
        flash('Failed to delete product!', 'danger')
    
    return redirect(url_for('products'))

@app.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    try:
        # First check if customer has any orders
        orders = db.fetch_data("SELECT order_id FROM Orders WHERE customer_id = %s", (customer_id,))
        
        if orders:
            # Delete associated orders first
            for order in orders:
                # Get order details to restore product stock
                order_details = db.fetch_data("""
                    SELECT product_id, quantity FROM OrderDetails WHERE order_id = %s
                """, (order['order_id'],))
                
                # Restore product stock quantities
                for detail in order_details:
                    db.execute_query("""
                        UPDATE Products 
                        SET stock_quantity = stock_quantity + %s 
                        WHERE product_id = %s
                    """, (detail['quantity'], detail['product_id']))
                
                # Delete order (OrderDetails will be deleted automatically due to CASCADE)
                db.execute_query("DELETE FROM Orders WHERE order_id = %s", (order['order_id'],))
        
        # Now delete the customer
        success = db.execute_query("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
        
        if success:
            flash('Customer and associated orders deleted successfully!', 'success')
        else:
            flash('Failed to delete customer!', 'danger')
            
    except mysql.connector.Error as err:
        db.conn.rollback()
        flash(f'Error deleting customer: {err}', 'danger')
    finally:
        db.close()
    
    return redirect(url_for('customers'))

@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    try:
        # Get order details to restore product stock
        order_details = db.fetch_data("""
            SELECT product_id, quantity FROM OrderDetails WHERE order_id = %s
        """, (order_id,))
        
        # Restore product stock quantities
        for detail in order_details:
            db.execute_query("""
                UPDATE Products 
                SET stock_quantity = stock_quantity + %s 
                WHERE product_id = %s
            """, (detail['quantity'], detail['product_id']))
        
        # Delete order (OrderDetails will be deleted automatically due to CASCADE)
        success = db.execute_query("DELETE FROM Orders WHERE order_id = %s", (order_id,))
        
        if success:
            flash('Order deleted successfully!', 'success')
        else:
            flash('Failed to delete order!', 'danger')
            
    except mysql.connector.Error as err:
        db.conn.rollback()
        flash(f'Error deleting order: {err}', 'danger')
    finally:
        db.close()
    
    return redirect(url_for('orders'))

@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        category_id = request.form.get('category_id')
        price = request.form.get('price')
        stock_quantity = request.form.get('stock_quantity')
        
        if product_name and category_id:
            query = """
            UPDATE Products 
            SET product_name = %s, category_id = %s, price = %s, stock_quantity = %s
            WHERE product_id = %s
            """
            success = db.execute_query(query, (product_name, category_id, price, stock_quantity, product_id))
            
            if success:
                flash('Product updated successfully!', 'success')
            else:
                flash('Failed to update product!', 'danger')
            
            db.close()
            return redirect(url_for('products'))
    
    # GET request - show edit form
    product = db.fetch_data("SELECT * FROM Products WHERE product_id = %s", (product_id,))[0]
    categories = db.fetch_data("SELECT * FROM Categories")
    db.close()
    
    return render_template('edit_product.html', product=product, categories=categories)

@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        description = request.form.get('description')
        
        if category_name:
            query = "UPDATE Categories SET category_name = %s, description = %s WHERE category_id = %s"
            success = db.execute_query(query, (category_name, description, category_id))
            
            if success:
                flash('Category updated successfully!', 'success')
            else:
                flash('Failed to update category!', 'danger')
            
            db.close()
            return redirect(url_for('categories'))
    
    # GET request - show edit form
    category = db.fetch_data("SELECT * FROM Categories WHERE category_id = %s", (category_id,))[0]
    db.close()
    
    return render_template('edit_category.html', category=category)

@app.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        address = request.form.get('address')
        
        if first_name and last_name:
            query = """
            UPDATE Customers 
            SET first_name = %s, last_name = %s, phone_number = %s, email = %s, address = %s
            WHERE customer_id = %s
            """
            success = db.execute_query(query, (first_name, last_name, phone_number, email, address, customer_id))
            
            if success:
                flash('Customer updated successfully!', 'success')
            else:
                flash('Failed to update customer!', 'danger')
            
            db.close()
            return redirect(url_for('customers'))
    
    # GET request - show edit form
    customer = db.fetch_data("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))[0]
    db.close()
    
    return render_template('edit_customer.html', customer=customer)

@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    
    if request.method == 'POST':
        status = request.form.get('status')
        
        query = "UPDATE Orders SET status = %s WHERE order_id = %s"
        success = db.execute_query(query, (status, order_id))
        
        if success:
            flash('Order updated successfully!', 'success')
        else:
            flash('Failed to update order!', 'danger')
        
        db.close()
        return redirect(url_for('orders'))
    
    # GET request - show edit form
    order = db.fetch_data("""
    SELECT o.*, CONCAT(c.first_name, ' ', c.last_name) as customer_name
    FROM Orders o
    JOIN Customers c ON o.customer_id = c.customer_id
    WHERE o.order_id = %s
    """, (order_id,))[0]
    
    order_details = db.fetch_data("""
    SELECT od.*, p.product_name
    FROM OrderDetails od
    JOIN Products p ON od.product_id = p.product_id
    WHERE od.order_id = %s
    """, (order_id,))
    
    db.close()
    
    return render_template('edit_order.html', order=order, order_details=order_details)

# View routes for categories, products, and customers

@app.route('/categories/view/<int:category_id>')
def view_category(category_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    category = db.fetch_data("SELECT * FROM Categories WHERE category_id = %s", (category_id,))[0]
    products = db.fetch_data("SELECT * FROM Products WHERE category_id = %s", (category_id,))
    db.close()
    
    return render_template('view_category.html', category=category, products=products)

@app.route('/products/view/<int:product_id>')
def view_product(product_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    product = db.fetch_data("""
        SELECT p.*, c.category_name 
        FROM Products p
        JOIN Categories c ON p.category_id = c.category_id
        WHERE p.product_id = %s
    """, (product_id,))[0]
    db.close()
    
    return render_template('view_product.html', product=product)

@app.route('/customers/view/<int:customer_id>')
def view_customer(customer_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    db = SaharaReadymadeDB()
    customer = db.fetch_data("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))[0]
    orders = db.fetch_data("""
        SELECT o.order_id, o.order_date, o.total_amount, o.status
        FROM Orders o
        WHERE o.customer_id = %s
        ORDER BY o.order_date DESC
    """, (customer_id,))
    db.close()
    
    return render_template('view_customer.html', customer=customer, orders=orders)

if __name__ == '__main__':
    app.run(debug=True)