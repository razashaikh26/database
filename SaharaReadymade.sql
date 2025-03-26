def create_order(self):
    # Order Creation Window
    order_window = tk.Toplevel(self.root)
    order_window.title("Create Order")
    order_window.geometry("600x400")

    # Fetch Customers and Products
    self.cursor.execute("SELECT customer_id, first_name, last_name FROM Customers")
    customers = self.cursor.fetchall()
    
    self.cursor.execute("SELECT product_id, product_name, price FROM Products")
    products = self.cursor.fetchall()

    # Customer Selection
    tk.Label(order_window, text="Select Customer:").pack()
    customer_var = tk.StringVar()
    customer_dropdown = ttk.Combobox(
        order_window, 
        textvariable=customer_var, 
        values=[f"{c['customer_id']} - {c['first_name']} {c['last_name']}" for c in customers]
    )
    customer_dropdown.pack()

    # Product Selection and Quantity
    tk.Label(order_window, text="Select Product:").pack()
    product_var = tk.StringVar()
    product_dropdown = ttk.Combobox(
        order_window, 
        textvariable=product_var, 
        values=[f"{p['product_id']} - {p['product_name']} (₹{p['price']})" for p in products]
    )
    product_dropdown.pack()

    tk.Label(order_window, text="Quantity:").pack()
    quantity_entry = tk.Entry(order_window)
    quantity_entry.pack()

    def submit_order():
        try:
            # Validate Customer Selection
            if not customer_var.get():
                messagebox.showerror("Error", "Please select a customer")
                return

            # Validate Product Selection
            if not product_var.get():
                messagebox.showerror("Error", "Please select a product")
                return

            # Validate Quantity
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive quantity")
                return

            # Safely extract IDs
            try:
                customer_id = int(customer_var.get().split(' - ')[0])
                product_id = int(product_var.get().split(' - ')[0])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid customer or product selection")
                return

            # Create Order
            self.cursor.execute("INSERT INTO Orders (customer_id) VALUES (%s)", (customer_id,))
            order_id = self.cursor.lastrowid

            # Get Product Price
            self.cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
            product_price = self.cursor.fetchone()['price']

            # Insert Order Details
            self.cursor.execute(
                "INSERT INTO OrderDetails (order_id, product_id, quantity, price_at_time) VALUES (%s, %s, %s, %s)",
                (order_id, product_id, quantity, product_price)
            )

            # Update Total Amount
            total_amount = quantity * product_price
            self.cursor.execute(
                "UPDATE Orders SET total_amount = %s WHERE order_id = %s", 
                (total_amount, order_id)
            )

            self.conn.commit()
            messagebox.showinfo("Success", f"Order Created! Order ID: {order_id}")
            
            # Clear the form after successful order
            customer_var.set('')
            product_var.set('')
            quantity_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.conn.rollback()

    tk.Button(order_window, text="Submit Order", command=submit_order).pack(pady=10)