import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from initialize_database import initialize_database

# Load environment variables
load_dotenv()

class SaharaReadymadeApp:
    def __init__(self):
        # Initialize session state for database connection
        if 'db_connection' not in st.session_state:
            try:
                st.session_state.db_connection = mysql.connector.connect(
                    host=os.environ.get("DB_HOST", "localhost"),
                    user=os.environ.get("DB_USER", "root"),
                    password=os.environ.get("DB_PASSWORD", ""),
                    database=os.environ.get("DB_NAME", "SaharaReadymade")
                )
                st.session_state.cursor = st.session_state.db_connection.cursor(dictionary=True)
                self.initialize_database()
            except mysql.connector.Error as err:
                st.error(f"Database Connection Error: {err}")
                st.stop()

    def initialize_database(self):
        """Ensure required columns exist in the database"""
        try:
            conn, cursor = self.get_connection()
            # Check if payment_status column exists
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Orders' AND COLUMN_NAME = 'payment_status'
            """)
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE Orders ADD COLUMN payment_status VARCHAR(20) DEFAULT 'Pending'")
                conn.commit()
        except mysql.connector.Error as err:
            st.error(f"Database initialization error: {err}")
            conn.rollback()

    def get_connection(self):
        return st.session_state.db_connection, st.session_state.cursor

    def fetch_data(self, query, params=None):
        conn, cursor = self.get_connection()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            st.error(f"Error fetching data: {err}")
            return []

    def execute_query(self, query, params=None):
        conn, cursor = self.get_connection()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            st.error(f"Error executing query: {err}")
            return False

    def manage_categories(self):
        st.header("📋 Category Management")

        # Fetch existing categories
        categories = self.fetch_data("SELECT * FROM Categories")
        if categories:
            st.dataframe(pd.DataFrame(categories))

        # Add new category
        with st.form("add_category_form"):
            st.subheader("Add New Category")
            category_name = st.text_input("Category Name")
            category_description = st.text_area("Description")
            submit_category = st.form_submit_button("Add Category")

            if submit_category:
                if category_name:
                    query = "INSERT INTO Categories (category_name, description) VALUES (%s, %s)"
                    if self.execute_query(query, (category_name, category_description)):
                        st.success("Category Added Successfully!")
                        st.rerun()
                else:
                    st.warning("Category Name is required!")

    def manage_products(self):
        st.header("🛍️ Product Management")

        # Fetch categories for dropdown
        categories = self.fetch_data("SELECT * FROM Categories")
        
        # Check if categories exist
        if not categories:
            st.warning("No categories found. Please add a category first.")
            return

        category_names = [cat['category_name'] for cat in categories]

        # Fetch existing products
        products = self.fetch_data("""
            SELECT p.*, c.category_name 
            FROM Products p
            JOIN Categories c ON p.category_id = c.category_id
        """)
        if products:
            st.dataframe(pd.DataFrame(products))

        # Add new product
        with st.form("add_product_form"):
            st.subheader("Add New Product")
            product_name = st.text_input("Product Name")
            category = st.selectbox("Category", category_names)
            price = st.number_input("Price", min_value=0.0, step=0.1)
            stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)

            submit_product = st.form_submit_button("Add Product")

            if submit_product:
                if product_name and category:
                    # Get category ID
                    category_query = "SELECT category_id FROM Categories WHERE category_name = %s"
                    category_result = self.fetch_data(category_query, (category,))
                    
                    if category_result:
                        category_id = category_result[0]['category_id']
                        query = """
                        INSERT INTO Products (product_name, category_id, price, stock_quantity) 
                        VALUES (%s, %s, %s, %s)
                        """
                        if self.execute_query(query, (product_name, category_id, price, stock_quantity)):
                            st.success("Product Added Successfully!")
                            st.rerun()
                    else:
                        st.error("Category not found!")
                else:
                    st.warning("Product Name and Category are required!")

    def manage_customers(self):
        st.header("👥 Customer Management")

        # Fetch existing customers
        customers = self.fetch_data("SELECT * FROM Customers")
        if customers:
            st.dataframe(pd.DataFrame(customers))

        # Add new customer
        with st.form("add_customer_form"):
            st.subheader("Add New Customer")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name")
            with col2:
                last_name = st.text_input("Last Name")
            
            phone_number = st.text_input("Phone Number")
            email = st.text_input("Email")
            address = st.text_area("Address")

            submit_customer = st.form_submit_button("Add Customer")

            if submit_customer:
                if first_name and last_name:
                    query = """
                    INSERT INTO Customers (first_name, last_name, phone_number, email, address) 
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    if self.execute_query(query, (first_name, last_name, phone_number, email, address)):
                        st.success("Customer Added Successfully!")
                        st.rerun()
                else:
                    st.warning("First Name and Last Name are required!")

    def create_order(self):
        st.header("🛒 Create Order")

        # Fetch customers and products
        customers = self.fetch_data("SELECT customer_id, first_name, last_name FROM Customers")
        products = self.fetch_data("SELECT product_id, product_name, price, stock_quantity FROM Products")

        # Check if there are any customers or products
        if not customers:
            st.warning("No customers found. Please add customers first.")
            return

        if not products:
            st.warning("No products found. Please add products first.")
            return

        # Customer Selection
        customer_options = {f"{c['customer_id']} - {c['first_name']} {c['last_name']}": c['customer_id'] for c in customers}
        selected_customer = st.selectbox("Select Customer", list(customer_options.keys()))

        # Product Selection
        product_options = {f"{p['product_id']} - {p['product_name']} (₹{p['price']})": p for p in products}
        
        # Validate product selection
        if not product_options:
            st.warning("No products available. Please add products first.")
            return

        # Ensure a default selection exists
        selected_product = st.selectbox("Select Product", list(product_options.keys()))

        # Additional safety check
        if not selected_product:
            st.warning("Please select a product.")
            return

        # Safely get the product
        product = product_options.get(selected_product)
        
        if not product:
            st.error("Invalid product selection.")
            return

        # Quantity Input
        max_quantity = product.get('stock_quantity', 0)
        
        if max_quantity <= 0:
            st.warning(f"Product '{product.get('product_name', 'Selected Product')}' is out of stock.")
            return

        quantity = st.number_input("Quantity", min_value=1, max_value=max_quantity, step=1)

        # Order Submission
        if st.button("Create Order"):
            try:
                conn, cursor = self.get_connection()
                
                # Check if there's an active transaction and rollback if needed
                if conn.in_transaction:
                    conn.rollback()
                
                # Start transaction
                conn.start_transaction()

                # Create Order with default payment status
                cursor.execute(
                    "INSERT INTO Orders (customer_id, payment_status) VALUES (%s, %s)", 
                    (customer_options[selected_customer], 'Pending')
                )
                order_id = cursor.lastrowid

                # Insert Order Details
                cursor.execute(
                    "INSERT INTO OrderDetails (order_id, product_id, quantity, price_at_time) VALUES (%s, %s, %s, %s)",
                    (order_id, product['product_id'], quantity, product['price'])
                )

                # Update Total Amount
                total_amount = quantity * product['price']
                cursor.execute(
                    "UPDATE Orders SET total_amount = %s WHERE order_id = %s", 
                    (total_amount, order_id)
                )

                # Reduce Product Stock
                cursor.execute(
                    "UPDATE Products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                    (quantity, product['product_id'])
                )

                # Commit transaction
                conn.commit()
                st.success(f"Order Created Successfully! Order ID: {order_id}")

            except mysql.connector.Error as err:
                # Rollback in case of error
                if conn.in_transaction:
                    conn.rollback()
                st.error(f"Error creating order: {err}")

    def view_orders(self):
        st.header("📦 Order History")

        # Fetch Orders with payment status
        orders = self.fetch_data("""
        SELECT o.order_id, 
               CONCAT(c.first_name, ' ', c.last_name) as customer_name, 
               o.order_date, 
               o.total_amount, 
               o.status,
               o.payment_status
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
        """)

        if not orders:
            st.info("No orders found.")
            return

        # Convert to DataFrame for better display
        orders_df = pd.DataFrame(orders)
        st.dataframe(orders_df)

        # Order Details Expander
        with st.expander("View Order Details"):
            selected_order = st.selectbox("Select Order", 
                [f"Order {order['order_id']} - {order['customer_name']}" for order in orders],
                key="order_details_select"
            )
            
            # Fetch specific order details
            order_id = int(selected_order.split(' - ')[0].split()[1])
            order_details = self.fetch_data("""
            SELECT p.product_name, od.quantity, od.price_at_time, 
                   (od.quantity * od.price_at_time) as subtotal
            FROM OrderDetails od
            JOIN Products p ON od.product_id = p.product_id
            WHERE od.order_id = %s
            """, (order_id,))

            if order_details:
                st.dataframe(pd.DataFrame(order_details))

        # Payment Status Update Section
        st.subheader("Update Payment Status")
        with st.form("payment_status_form"):
            # Get order IDs and current statuses
            order_options = [f"{order['order_id']} - {order['customer_name']} (Current: {order['payment_status']})" 
                           for order in orders]
            
            selected_order_for_payment = st.selectbox(
                "Select Order to Update",
                order_options,
                key="payment_order_select"
            )
            
            # Extract order ID from selection
            order_id_for_payment = int(selected_order_for_payment.split(' - ')[0])
            
            # Get current payment status for selected order
            current_status = next(
                (order['payment_status'] for order in orders 
                 if order['order_id'] == order_id_for_payment),
                "Pending"
            )
            
            new_payment_status = st.selectbox(
                "New Payment Status",
                ["Pending", "Paid", "Partially Paid", "Cancelled", "Refunded"],
                index=["Pending", "Paid", "Partially Paid", "Cancelled", "Refunded"].index(current_status)
                if current_status in ["Pending", "Paid", "Partially Paid", "Cancelled", "Refunded"]
                else 0
            )
            
            update_payment_button = st.form_submit_button("Update Payment Status")
            
            if update_payment_button:
                try:
                    query = "UPDATE Orders SET payment_status = %s WHERE order_id = %s"
                    if self.execute_query(query, (new_payment_status, order_id_for_payment)):
                        st.success(f"Payment status for Order {order_id_for_payment} updated to {new_payment_status}!")
                        st.rerun()
                    else:
                        st.error("Failed to update payment status.")
                except Exception as e:
                    st.error(f"Error updating payment status: {str(e)}")

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Sahara Readymade Store Management",
        page_icon="🛍️",
        layout="wide"
    )

    # Initialize the database if needed
    try:
        initialize_database()
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")

    # Create app instance
    app = SaharaReadymadeApp()

    # Sidebar Navigation
    st.sidebar.title("🏪 Sahara Readymade")
    menu_options = [
        "Manage Categories", 
        "Manage Products", 
        "Manage Customers", 
        "Create Order", 
        "View Orders"
    ]
    choice = st.sidebar.radio("Navigation", menu_options)

    # Routing
    if choice == "Manage Categories":
        app.manage_categories()
    elif choice == "Manage Products":
        app.manage_products()
    elif choice == "Manage Customers":
        app.manage_customers()
    elif choice == "Create Order":
        app.create_order()
    elif choice == "View Orders":
        app.view_orders()

if __name__ == "__main__":
    main()