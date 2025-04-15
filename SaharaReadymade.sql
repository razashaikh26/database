import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

class SaharaReadymadeApp:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Razashaikh@12',
            'database': 'SaharaReadymade'
        }

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def fetch_data(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def execute_query(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            conn.commit()
            return True
        except mysql.connector.Error as err:
            st.error(f"Database error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def manage_categories(self):
        """Manage product categories"""
        try:
            st.header("📦 Manage Categories")
            
            # Display existing categories
            categories = self.fetch_data("SELECT * FROM Categories")
            if categories:
                st.dataframe(pd.DataFrame(categories))
            else:
                st.info("No categories found")
            
            # Add new category
            st.subheader("Add New Category")
            with st.form("category_form"):
                name = st.text_input("Category Name")
                description = st.text_area("Description")
                
                if st.form_submit_button("Add Category"):
                    if name:
                        if self.execute_query(
                            "INSERT INTO Categories (category_name, description) VALUES (%s, %s)",
                            (name, description)
                        ):
                            st.success("Category added successfully!")
                            st.rerun()
                    else:
                        st.warning("Category name is required")
        except Exception as e:
            st.error(f"Error in manage_categories: {e}")

    def manage_products(self):
        """Manage products"""
        try:
            st.header("👕 Manage Products")
            
            # Display existing products
            products = self.fetch_data("""
                SELECT p.*, c.category_name 
                FROM Products p
                LEFT JOIN Categories c ON p.category_id = c.category_id
            """)
            if products:
                st.dataframe(pd.DataFrame(products))
            else:
                st.info("No products found")
            
            # Add new product
            st.subheader("Add New Product")
            categories = self.fetch_data("SELECT category_id, category_name FROM Categories")
            category_options = {c['category_name']: c['category_id'] for c in categories}
            
            with st.form("product_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Product Name")
                    category = st.selectbox("Category", list(category_options.keys()))
                    price = st.number_input("Price", min_value=0.0, step=0.01)
                with col2:
                    stock = st.number_input("Stock Quantity", min_value=0, step=1)
                    size = st.text_input("Size (optional)")
                    color = st.text_input("Color (optional)")
                
                if st.form_submit_button("Add Product"):
                    if name and price is not None and stock is not None:
                        category_id = category_options[category]
                        if self.execute_query(
                            """INSERT INTO Products 
                            (product_name, category_id, price, stock_quantity, size, color) 
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                            (name, category_id, price, stock, size, color)
                        ):
                            st.success("Product added successfully!")
                            st.rerun()
                    else:
                        st.warning("Product name, price, and stock are required")
        except Exception as e:
            st.error(f"Error in manage_products: {e}")

    def manage_customers(self):
        """Manage customers"""
        try:
            st.header("👥 Manage Customers")
            
            # Display existing customers
            customers = self.fetch_data("SELECT * FROM Customers")
            if customers:
                st.dataframe(pd.DataFrame(customers))
            else:
                st.info("No customers found")
            
            # Add new customer
            st.subheader("Add New Customer")
            with st.form("customer_form"):
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    phone = st.text_input("Phone Number")
                with col2:
                    email = st.text_input("Email")
                    address = st.text_area("Address")
                
                if st.form_submit_button("Add Customer"):
                    if first_name and last_name:
                        if self.execute_query(
                            """INSERT INTO Customers 
                            (first_name, last_name, phone_number, email, address) 
                            VALUES (%s, %s, %s, %s, %s)""",
                            (first_name, last_name, phone, email, address)
                        ):
                            st.success("Customer added successfully!")
                            st.rerun()
                    else:
                        st.warning("First name and last name are required")
        except Exception as e:
            st.error(f"Error in manage_customers: {e}")

    def view_orders(self):
        """View all orders"""
        try:
            st.header("📋 Order History")
            
            orders = self.fetch_data("""
                SELECT o.order_id, 
                       CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                       o.order_date,
                       o.total_amount,
                       o.status,
                       o.payment_status,
                       o.payment_date
                FROM Orders o
                JOIN Customers c ON o.customer_id = c.customer_id
                ORDER BY o.order_date DESC
            """)
            
            if orders:
                st.dataframe(pd.DataFrame(orders))
            else:
                st.info("No orders found")
        except Exception as e:
            st.error(f"Error in view_orders: {e}")

    def create_order(self):
        """Create new orders with payment status"""
        try:
            st.header("🛒 Create Order")

            # Fetch customers and products
            customers = self.fetch_data("SELECT customer_id, first_name, last_name FROM Customers")
            products = self.fetch_data("SELECT product_id, product_name, price, stock_quantity FROM Products")

            if not customers:
                st.warning("No customers found. Please add customers first.")
                return
                
            if not products:
                st.warning("No products found. Please add products first.")
                return

            # Customer selection
            customer_options = {f"{c['customer_id']} - {c['first_name']} {c['last_name']}": c['customer_id'] for c in customers}
            selected_customer_key = st.selectbox("Select Customer", list(customer_options.keys()), key="order_cust")
            selected_customer_id = customer_options[selected_customer_key]

            # Product selection
            product_options = {f"{p['product_id']} - {p['product_name']} (₹{p['price']})": p for p in products}
            selected_product_key = st.selectbox("Select Product", list(product_options.keys()), key="order_prod")
            selected_product = product_options[selected_product_key]

            # Quantity input
            max_quantity = selected_product['stock_quantity']
            quantity = st.number_input(
                "Quantity", 
                min_value=1, 
                max_value=max_quantity if max_quantity > 0 else 1, 
                step=1,
                key="order_qty"
            )
            
            # Display total amount
            total_amount = quantity * selected_product['price']
            st.markdown(f"**Total Amount: ₹{total_amount:.2f}**")

            # Simple payment status (Paid/Pending)
            is_paid = st.checkbox("Mark as Paid", key="payment_status")

            # Order submission
            if st.button("Create Order", key="order_submit"):
                conn = self.get_connection()
                cursor = conn.cursor()
                try:
                    conn.start_transaction()
                    
                    # Create order with payment status
                    payment_status = "Paid" if is_paid else "Pending"
                    cursor.execute(
                        """INSERT INTO Orders 
                        (customer_id, total_amount, payment_status) 
                        VALUES (%s, %s, %s)""",
                        (selected_customer_id, total_amount, payment_status)
                    )
                    order_id = cursor.lastrowid

                    # Add order details
                    cursor.execute(
                        """INSERT INTO OrderDetails 
                        (order_id, product_id, quantity, price_at_time) 
                        VALUES (%s, %s, %s, %s)""",
                        (order_id, selected_product['product_id'], quantity, selected_product['price'])
                    )

                    # Update product stock
                    cursor.execute(
                        """UPDATE Products 
                        SET stock_quantity = stock_quantity - %s 
                        WHERE product_id = %s""",
                        (quantity, selected_product['product_id'])
                    )

                    conn.commit()
                    status_msg = "and paid" if is_paid else "(payment pending)"
                    st.success(f"Order created successfully {status_msg}! Order ID: {order_id}")
                    st.rerun()
                except mysql.connector.Error as err:
                    conn.rollback()
                    st.error(f"Error creating order: {err}")
                finally:
                    cursor.close()
                    conn.close()
        except Exception as e:
            st.error(f"Error in create_order: {e}")

    def manage_payments(self):
        """Manage and update payment statuses"""
        try:
            st.header("💳 Payment Management")

            # Fetch orders with pending payments
            pending_orders = self.fetch_data("""
                SELECT o.order_id, 
                       CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                       o.total_amount,
                       o.order_date
                FROM Orders o
                JOIN Customers c ON o.customer_id = c.customer_id
                WHERE o.payment_status = 'Pending'
                ORDER BY o.order_date DESC
            """)

            if pending_orders:
                st.subheader("Pending Payments")
                st.dataframe(pd.DataFrame(pending_orders))

                # Payment update form
                with st.form("update_payment"):
                    selected_order = st.selectbox(
                        "Select Order to Update",
                        [f"Order #{o['order_id']} - {o['customer_name']} (₹{o['total_amount']})" 
                         for o in pending_orders],
                        key="select_pending_order"
                    )
                    order_id = int(selected_order.split('#')[1].split()[0])
                    
                    if st.form_submit_button("Mark as Paid"):
                        if self.execute_query(
                            """UPDATE Orders 
                            SET payment_status = 'Paid', 
                                payment_date = CURRENT_TIMESTAMP 
                            WHERE order_id = %s""",
                            (order_id,)
                        ):
                            st.success(f"Order #{order_id} marked as Paid")
                            st.rerun()
            else:
                st.info("No pending payments found")

            # Payment history
            st.subheader("Payment History")
            payments = self.fetch_data("""
                SELECT o.order_id,
                       CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                       o.total_amount,
                       o.payment_status,
                       o.payment_date
                FROM Orders o
                JOIN Customers c ON o.customer_id = c.customer_id
                WHERE o.payment_status = 'Paid'
                ORDER BY o.payment_date DESC
            """)
            
            if payments:
                st.dataframe(pd.DataFrame(payments))
        except Exception as e:
            st.error(f"Error in manage_payments: {e}")

def main():
    st.set_page_config(
        page_title="Sahara Readymade Store Management",
        page_icon="🛍️",
        layout="wide"
    )

    try:
        app = SaharaReadymadeApp()

        st.sidebar.title("🏪 Sahara Readymade")
        menu_options = [
            "Manage Categories", 
            "Manage Products", 
            "Manage Customers", 
            "Create Order", 
            "Manage Payments",
            "View Orders"
        ]
        choice = st.sidebar.radio("Navigation", menu_options)

        if choice == "Manage Categories":
            app.manage_categories()
        elif choice == "Manage Products":
            app.manage_products()
        elif choice == "Manage Customers":
            app.manage_customers()
        elif choice == "Create Order":
            app.create_order()
        elif choice == "Manage Payments":
            app.manage_payments()
        elif choice == "View Orders":
            app.view_orders()

    except Exception as e:
        st.error(f"Application error: {e}")

if __name__ == "__main__":
    main()