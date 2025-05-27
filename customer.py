import mysql.connector
import csv
import pandas as pd

class Customer:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db.cursor()

    def validate_customer(self,phone):

        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone Number Should be 10_Digits")

    def customer_exists(self, cid):
        self.cursor.execute("select * from customers where customer_id = %s", (cid,))
        return self.cursor.fetchone() is not None
    
    @staticmethod
    def confirm(prompt="Are you sure? (Y/N): "):
        while True:
            choice = input(prompt).lower()
            if choice in ['y','Y', 'yes']:
                return True
            elif choice in ['n','N', 'no']:
                return False
            else:
                print("Please enter 'Y' or 'N'.")

    def generate_customer_id(self):
        try:
            self.cursor.execute("SELECT customer_id FROM customers ORDER BY customer_id DESC LIMIT 1")
            result = self.cursor.fetchone()
            if result and result[0]:
                last_id = int(result[0][5:])
                new_id = f"CUST-{last_id + 1:03d}"
            else:
                new_id = "CUST-001"
            return new_id
        except mysql.connector.Error as err:
            print("Error generating customer ID:", err)
            return None

    def add_customer(self, name, phone):
        try:

            customer_id = self.generate_customer_id()
            if not customer_id:
                print("Customer ID generation failed.")
                return
            sql = "INSERT INTO customers (customer_id, name, phone) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (customer_id, name, phone))
            self.db.commit()
            print(f"Customer '{name}' added with ID: {customer_id}")
            print("\n Customer details registered Successfully")
        except mysql.connector.Error as err:
            print("Error registering the customer details:", err)

    def get_all_customers(self):
        try:
            self.cursor.execute("SELECT * FROM customers")
            rows = self.cursor.fetchall()
            if rows:
                print("\n--- Customer Details ---")
                for row in rows:
                    print(f"ID: {row[0]}, Name: {row[1]},Phone: {row[2]}")
            else:
                print("No customer details found.")
        except Exception as e:
            print("Failed to retrieve customer details:", e)

    def update_customer(self, customer_id, name=None, phone=None):
        try:
            updates = []
            params = []

            if name:
                updates.append("name = %s")
                params.append(name)

            if phone:
                updates.append("phone = %s")
                params.append(phone)

            if not updates:
                print("No fields to update.")
                return

            query = f"UPDATE customers SET {', '.join(updates)} WHERE customer_id = %s"
            params.append(customer_id)

            self.cursor.execute(query, tuple(params))
            self.db.commit()
            print("Customer details updated successfully.")
        except Exception as e:
            print("Failed to update customer details:", e)

    def delete_customer(self, customer_id):
        if Customer.confirm("Are you sure you want to delete this Customer (Y/N)?"):
            query="DELETE FROM customers WHERE customer_id = %s"
            try:
                self.cursor.execute(query, (customer_id,))
                self.db.commit()
                if self.cursor.rowcount > 0:
                    print("Customer details deleted successfully.")
                else:
                    print("No customer found.")
            except Exception as e:
                print("Failed to delete customer details:", e)

    def export_to_csv(self, filename="data/customers.csv"):
        try:
            self.cursor.execute("select * from customers")
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=["customer_id", "name", "phone"])
            df.to_csv(filename, index=False)
            print("Customer details exported successfully.")
        except Exception as e:
            print(f"Exporting failed: {e}")

    def import_from_csv(self, filename="data/customers.csv"):
        try:
            df = pd.read_csv(filename)
            for _, row in df.iterrows():
                self.cursor.execute(
                    "insert into customers (customer_id, name, phone) values (%s, %s, %s)",
                    (row["customer_id"], row["name"], row["phone"])
                )
                self.db.commit()
            print("product details imported successfully.")
        except Exception as e:
            print(f"Importing failed: {e}")
