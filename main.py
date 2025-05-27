from db_config import create_connection
from product import Product
from customer import Customer
from sales import Sale
from billing import Billing

def product_menu(product_manager):
    while True:
        print("\n=== Product Management===")
        print("1. Add New Product ")
        print("2. View All Products")
        print("3. Update A Product")
        print("4. Delete A Product")
        print("5. Search A Product")
        print("6. Show Stock Alerts of Products")
        print("7. Return to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter Product Name: ")
            category = input("Enter Product Category: ")
            price = float(input("Enter Product Price: "))
            quantity = int(input("Enter Total Quantity: "))
            product_manager.add_product(name, category, price, quantity)

        elif choice == "2":
            product_manager.view_products()

        elif choice == "3":
            pid = input("Enter Product ID to Update: ")
            name = input("Update Name (or press Enter to use existing ): ")
            category = input("Update Category (or press Enter to use existing): ")
            price = input("Update Price (or press Enter to use existing): ")
            quantity = input("Update Quantity (or press Enter to use existing): ")
            product_manager.update_product(
                pid,
                name=name,
                category=category,
                price=float(price) if price else None,
                quantity=int(quantity) if quantity else None
            )

        elif choice == "4":
            pid = input("Enter Product ID to Delete: ")
            product_manager.delete_product(pid)

        elif choice == "5":
            product_manager.search_product()

        elif choice == '6':
            try:
                threshold = int(input("Enter stock threshold (default is 5): ") or "5")
            except ValueError:
                threshold = 5
            product_manager.stock_alerts(low_stock_threshold=threshold)

        elif choice == "7":
            break

        else:
            print("Invalid choice. Please try again.")


def customer_menu(customer_manager):
    while True:
        print("\n=== Customer Management ===")
        print("1. Add New Customer")
        print("2. View All Customers")
        print("3. Update A Customer")
        print("4. Delete A Customer")
        print("5. Return to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter Customer Name: ")
            phone = input("Enter Phone Number: ")
            customer_manager.validate_customer(phone)
            customer_manager.add_customer(name, phone)

        elif choice == "2":
            customer_manager.get_all_customers()

        elif choice == "3":
            cid = input("Enter Customer ID to Update: ")
            name = input("Update Name (press Enter to use existing): ")
            phone = input("Update Phone (press Enter to use existing): ")
            customer_manager.update_customer(cid, name, phone)

        elif choice == "4":
            cid = input("Enter customer ID to delete: ")
            customer_manager.delete_customer(cid)

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def sales_menu(sales_manager):
    while True:
        print("\n=== Sales Menu ===")
        print("1. Record a Sale")
        print("2. View All Sales")
        print("3. View Daily Sales Summary")
        print("4. View Monthly Sales Summary")
        print("5. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_id = input("Enter Customer ID: ")
            product_id = input("Enter Product ID: ")
            quantity = int(input("Enter Total Qunatity Sold: "))
            sales_manager.record_sale(customer_id, product_id,quantity)

        elif choice == "2":
            sales_manager.get_all_sales()

        elif choice == "3":
            sales_manager.daily_summary()

        elif choice == '4':
            year=int(input("Enter Year [YYYY]: "))
            month=int(input("Enter Month [1-12]"))
            sales_manager.monthly_summary(year,month)

        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def billing_menu(billing_manager):
    while True:
        print("\n=== Billing Menu ===")
        print("1. Generate Bill by Customer ID")
        print("2. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_id = input("Enter Customer ID: ")
            billing_manager.generate_bill_by_customer(customer_id)

        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

def csv_menu(product_manager,customer_manager,sales_manager):

    while True:
        print("\n ==== CSV Files ====")
        print("1. Export Product CSV ")
        print("2. import Product CSV ")
        print("3. Export Customer CSV ")
        print("4. import Customer CSV ")
        print("5. Export Sales CSV ")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            product_manager.export_to_csv()

        elif choice == "2":
            product_manager.import_from_csv()

        elif choice == "3":
            customer_manager.export_to_csv()

        elif choice == "4":
            customer_manager.import_from_csv()

        elif choice == '5':
            sales_manager.export_sales_to_csv()

        elif choice == "6":
            print("Return to main menu")
            break
        else:
            print("Invalid choice. Please try again.")



def main():
    conn = create_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    product_manager = Product(conn)
    customer_manager = Customer(conn)
    sales_manager = Sale(conn)
    billing_manager = Billing(conn)

    while True:
        print("\n=== Inventory and Sales System ===")
        print("1. Manage Products Records")
        print("2. Manage Customers Records")
        print("3. Process Sales Records")
        print("4. Generate Bills Records")
        print("5. Manage Import/Export")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_menu(product_manager)
        elif choice == "2":
            customer_menu(customer_manager)
        elif choice == "3":
            sales_menu(sales_manager)
        elif choice == "4":
            billing_menu(billing_manager)
        elif choice == "5":
            csv_menu(product_manager,customer_manager,sales_manager)
        elif choice == "6":
            print("Thank you. Bye!")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()


if __name__ == "__main__":
    main()
