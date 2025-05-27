import mysql.connector
import csv
import pandas as pd

class Product:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db.cursor()

    def generate_product_id(self):
        try:
            self.cursor.execute("SELECT product_id FROM products ORDER BY product_id DESC LIMIT 1")
            result = self.cursor.fetchone()
            if result and result[0]:
                last_id = int(result[0][3:])
                new_id = f"PRD{last_id + 1:03d}"
            else:
                new_id = "PRD001"
            return new_id
        except mysql.connector.Error as err:
            print("Error generating product ID:", err)
            return None

    def add_product(self, name, category, price, quantity):
        try:
            product_id = self.generate_product_id()
            if not product_id:
                print("Failed to generate product ID.")
                return
            sql = "INSERT INTO products (product_id, name, category, price, quantity) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (product_id, name, category, price, quantity))
            self.db.commit()
            print(f"Product '{name}' added with ID: {product_id}")
            print("\n Product details added Successfully")
        except mysql.connector.Error as err:
            print("Error adding product details:", err)

    def view_products(self):
        try:
            query = "SELECT * FROM products"
            self.cursor.execute(query)
            products = self.cursor.fetchall()
            if len(products)==0:
                print("No products details found")
            else:
                print("\n--- Product Details ---")
                for product in products:
                    print(
                        f"ID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: {product[3]}, Quantity: {product[4]}")
        except mysql.connector.Error as err:
            print("Error viewing product details:", err)

    def update_product(self, product_id, name=None, category=None, price=None, quantity=None):
        try:
            updates = []
            values = []
            if name:
                updates.append("name=%s")
                values.append(name)
            if category:
                updates.append("category=%s")
                values.append(category)
            if price is not None:
                updates.append("price=%s")
                values.append(price)
            if quantity is not None:
                updates.append("quantity=%s")
                values.append(quantity)

            values.append(product_id)
            sql = f"UPDATE products SET {', '.join(updates)} WHERE product_id = %s"
            self.cursor.execute(sql, tuple(values))
            self.db.commit()
            print("Product details updated successfully.")
        except mysql.connector.Error as err:
            print("Error updating product details:", err)

    def delete_product(self, product_id):
        try:
            query = "DELETE FROM products WHERE product_id = %s"
            self.cursor.execute(query, (product_id,))
            self.db.commit()
            if self.cursor.rowcount>0:
                print("Product details deleted successfully.")
            else:
                print("No product found.")
        except mysql.connector.Error as err:
            print("Error deleting product details:", err)

    def search_product(self):
        try:
            search_by = input("Search By Category or Name of Product:").strip().lower()
            if search_by == "category":
                category =input("Enter Category Name: ").strip()
                query = "select * from products where category= %s "
                self.cursor.execute(query,(category,),)
            elif search_by == "name":
                name =input("Enter The Product Name: ").strip()
                query = "select * from products where name= %s "
                self.cursor.execute(query,(name,))
            else:
                print("Invalid option .Please Choose 'category' or 'name' of the product.")
                return
            products1 = self.cursor.fetchall()
            if not products1:
                print("Products not found.")
            else:
                for p in products1:
                    print(f"PID:{p[0]}, Name:{p[1]}, Category:{p[2]}, Price:{p[3]}, Quantity:{p[4]}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.cursor.close()
            self.db.close()

    def export_to_csv(self, filename="data/products.csv"):
        try:
            self.cursor.execute("select * from products")
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows, columns=["product_id", "name", "category", "price", "quantity"])
            df.to_csv(filename, index=False)
            print("Product details exported successfully.")
        except Exception as e:
            print(f"Exporting failed: {e}")

    def import_from_csv(self, filename="data/products.csv"):
        try:
            df = pd.read_csv(filename)
            for _, row in df.iterrows():
                self.cursor.execute(
                    "insert into products (product_id, name, category, price, quantity) values (%s, %s, %s, %s, %s)",
                    (row["product_id"], row["name"], row["category"], float(row["price"]), int(row["quantity"]))
                )
                self.db.commit()
            print("Product details imported successfully.")
        except Exception as e:
            print(f"Importing failed: {e}")

    def stock_alerts(self, low_stock_threshold=5):
        try:
            self.cursor.execute("SELECT product_id, name, quantity FROM products")
            products = self.cursor.fetchall()
            out_of_stock = []
            low_stock = []
            for pid, name, qty in products:
                if qty == 0:
                    out_of_stock.append((pid, name))
                elif qty <= low_stock_threshold:
                    low_stock.append((pid, name, qty))
            if out_of_stock:
                print("\n=== Out-of-Stock Products ===")
                for pid, name in out_of_stock:
                    print(f"ID: {pid}, Name: {name} (OUT OF STOCK)")
            if low_stock:
                print("\n=== Low-Stock Products ===")
                for pid, name, qty in low_stock:
                    print(f"ID: {pid}, Name: {name}, Quantity: {qty}")
            if not out_of_stock and not low_stock:
                print("\nAll products are sufficiently stocked.")
        except mysql.connector.Error as err:
            print("Error checking stock alerts:", err)
