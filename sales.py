import mysql.connector
from billing import Billing
import pandas as pd
from datetime import date,datetime
import csv

class Sale:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db.cursor()

    def record_sale(self, customer_id, product_id, quantity):
        try:

            self.cursor.execute("SELECT quantity FROM products WHERE product_id = %s", (product_id,))
            stock = self.cursor.fetchone()
            if not stock or stock[0] < quantity:
                self.db.rollback()
                raise ValueError("Insufficient stock")

            query = """
                    INSERT INTO sales (customer_id, product_id, quantity,sale_date)
                    VALUES (%s, %s, %s, %s)
            """
            values = (customer_id, product_id, quantity, date.today())
            self.cursor.execute(query, values)
            sale_id = self.cursor.lastrowid

            self.cursor.execute(
                "UPDATE products SET quantity = quantity - %s WHERE product_id = %s",
                (quantity, product_id)
            )

            self.db.commit()
            print("Sales registered successfully.")

            Billing(self.db).generate_invoice(sale_id)
        except ValueError as ve:
            print("Stock error:", ve)
        except mysql.connector.Error as err:
            self.db.rollback()
            print("Database error during sale:", err)

    def get_all_sales(self):
        try:
            query = "select * from sales"
            self.cursor.execute(query)
            sales = self.cursor.fetchall()
            print("\n--- Sales Details ---")
            if len(sales)==0:
                print("No sales found")
            else:
                for sale in sales:
                    sale_id = sale[0]
                    customer_id = sale[1]
                    product_id = sale[2]
                    quantity = sale[3]
                    sale_date = sale[4]

                    if isinstance(sale_date, (date,)):
                        sale_date_str = sale_date.strftime('%Y-%m-%d')
                    else:
                        sale_date_str = str(sale_date)
                    print(
                        f"sale_id: {sale_id}, customer_id: {customer_id}, product_id: {product_id}, quantity: {quantity}, sale_date: {sale_date_str}")
        except mysql.connector.Error as err:
            print("Error viewing Sales:", err)

    def daily_summary(self):
        try:
            self.cursor.execute("""
            SELECT p.name, SUM(s.quantity) AS total_sold
                    FROM sales s
                    JOIN products p ON s.product_id = p.product_id
                    WHERE s.sale_date = CURDATE()
                    GROUP BY p.name
            """)
            print("\nDaily Sales Summary:")
            for row in self.cursor.fetchall():
                print(f"Product: {row[0]}, Quantity Sold: {row[1]}")
        except Exception as e:
            print("Error fetching daily summary:", e)

    def monthly_summary(self, year, month):
        try:
            query = """
             SELECT p.name, SUM(s.quantity)
                     FROM sales s
                     JOIN products p ON s.product_id = p.product_id
                     WHERE YEAR(s.sale_date) = %s AND MONTH(s.sale_date) = %s
                     GROUP BY p.name
                 """
            self.cursor.execute(query, (year, month))
            print(f"\nMonthly Summary ({month}/{year}):")
            for row in self.cursor.fetchall():
                print(f"Product: {row[0]}, Quantity Sold: {row[1]}")
        except Exception as e:
            print("Error fetching monthly summary:", e)

    def export_sales_to_csv(self):
        try:
            self.cursor.execute("""
                SELECT s.sale_id, c.customer_id AS customer, p.product_id AS product, s.quantity, s.sale_date
                FROM sales s
                JOIN customers c ON s.customer_id = c.customer_id
                JOIN products p ON s.product_id = p.product_id
                ORDER BY s.sale_date
            """)
            rows = self.cursor.fetchall()
            columns = ["Sale ID", "Customer", "Product", "Quantity", "Sale Date"]
            df = pd.DataFrame(rows, columns=columns)
            filename = "Data/sales.csv"
            df.to_csv(filename, index=False)
            print(f"Sales exported to {filename}")
        except Exception as e:
            print("Error exporting sales:", e)
