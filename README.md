***Inventory and Sales Tracking System for a Retail Store***
This project implements a backend system for managing inventory and tracking sales in a retail store, accessible via a command-line interface (CLI).

Problem Statement:-
Efficiently managing stock inventory and tracking daily sales is crucial for modern retail operations. This system addresses the need for store managers to:
 * Manage products and customer records.
 * Track stock in real-time.
 * Record and analyze sales.
 * Generate bills and sales reports.

Objectives:-
The primary objectives of this project are to:
 * Design a modular Python application for managing products, customers, and sales.
 * Store and retrieve data using a MySQL relational database.
 * Implement real-time stock updates and reporting.
 * Apply object-oriented design principles.
 * Incorporate file (CSV) import/export features.

Technology Stack:-
 * Language: Core Python (OOP, File Handling, Exception Handling)
 * Database: MySQL
 * Libraries: mysql-connector-python, pandas, datetime

Database Design:-
The system utilizes the following tables in the MySQL database:
1. products
Stores product information.
product_id: Unique identifier for each product.
name: Name of the product.
category: Classification of the product.
price: Cost of the product.
quantity: Available stock.
2. customers
Stores customer details.
customer_id: Unique identifier for each customer.
name: Customer's name.
phone: Contact number.
3. sales
Tracks transactions.
sale_id: Unique identifier for each sale (auto-incremented).
customer_id: Reference to the customer who made the purchase.
product_id: Reference to the purchased product.
quantity: Number of units sold.
sale_date: Date of purchase.
Each table should contain a minimum of 250 records.

Modules:-
The application is structured into the following modules:
 * Database connection module
 * Product management
 * Customer management
 * Sales processing
 * Billing and Reporting
 * CSV import/export
 * Main CLI dashboard

Key Features:-
The system implements the following functionalities:
 * Database Schema Design: Includes ER diagram and MySQL schema creation.
 * Database Connection: A dedicated db_config.py module handles Python-MySQL integration.
 * Product Management: Product class with add, view, update, and delete methods, including searching by category or name.
 * Customer Management: Customer class with add, view, and delete methods.
 * Sales Processing: Sale class to record new sales with real-time stock updates.
 * ID Generation: Auto-generation of unique customer and product IDs.
 * Billing: Generation of customer invoices after every sale, calculation of total amount, and application of basic tax (e.g., 5%).
 * Reporting: Daily/monthly sales summaries.
 * Data Import/Export: Export stock and sales data to CSV files and import product/customer data from CSV into MySQL.
 * Alerts: Display out-of-stock or low-stock alerts.
 * CLI: Command-line interface for user interaction and navigation.
 * Error Handling: Input validation and exception handling for robust user interaction.

Project Folder Structure:-
inventory_sales/
├── db_config.py
├── product.py
├── customer.py
├── sales.py
├── billing.py
├── main.py
├── data/
│   ├── products.csv
│   ├── customers.csv
│   └── sales.csv
├── reports/
├── invoices/
└── schema.sql
└── README.md
 
Key Deliverables:-
 * Full source code of the Python project.
 * MySQL schema file with sample data.
 * Sample input/output files (CSV).
 * User manual with CLI instructions.
 * Screenshots or recording of working demo (optional).
 