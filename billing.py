import os
from datetime import datetime
import mysql.connector
from decimal import Decimal


class Billing:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db.cursor()
        self.invoice_dir = 'reports/invoices/'
        os.makedirs(self.invoice_dir, exist_ok=True)

    def generate_invoice(self, sale_id):
        try:
            self.cursor.execute("""
                SELECT s.sale_id, c.name, c.phone, p.name, p.price, s.quantity, s.sale_date
                FROM sales s
                JOIN customers c ON s.customer_id = c.customer_id
                JOIN products p ON s.product_id = p.product_id
                WHERE s.sale_id = %s
            """, (sale_id,))
            result = self.cursor.fetchone()

            if not result:
                raise ValueError("Sale not found")

            sale_id, cust_name, phone, prod_name, price, qty, sale_date = result
            total = price * qty
            tax = total * Decimal('0.05')
            grand_total = total + tax

            # Create invoice content
            invoice_content = f"""
            ==========================================
                            INVOICE
            ==========================================

            Invoice ID     : {sale_id}
            Date           : {sale_date.strftime('%Y-%m-%d') if hasattr(sale_date, 'strftime') else sale_date}

            Customer Name  : {cust_name}
            Phone Number   : {phone}

            ------------------------------------------
            Product Details
            ------------------------------------------
            Product Name   : {prod_name}
            Quantity       : {qty}
            Unit Price     : ₹{price:.2f}
            ------------------------------------------
            Subtotal       : ₹{total:.2f}
            Tax (5%)       : ₹{tax:.2f}
            ------------------------------------------
            Grand Total    : ₹{grand_total:.2f}
            ==========================================

                Thank you for your purchase!
            ==========================================
            """

            # Print to console
            print(invoice_content)

            # Ensure invoice directory exists
            os.makedirs(self.invoice_dir, exist_ok=True)

            # Write invoice to file with UTF-8 encoding
            file_path = os.path.join(self.invoice_dir, f"invoice_{sale_id}.txt")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(invoice_content)

        except ValueError as ve:
            print("Invoice error:", ve)
        except mysql.connector.Error as err:
            print("Database error in invoice generation:", err)
        except IOError as io_err:
            print("File write error:", io_err)

    def generate_bill_by_customer(self, customer_id):
        try:
            self.cursor.execute("SELECT sale_id FROM sales WHERE customer_id = %s", (customer_id,))
            sale_ids = self.cursor.fetchall()
            if not sale_ids:
                print("No sales found for this customer.")
                return
            for (sale_id,) in sale_ids:
                self.generate_invoice(sale_id)
            print(f"Invoices generated for customer {customer_id}.")
        except mysql.connector.Error as err:
            print("Database error in generating bills by customer:", err)