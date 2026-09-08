# 🛒 E-Commerce Database Management System

## 📌 Project Overview

This project is a relational **E-Commerce Database Management System** developed using **MySQL**.

The database is designed to manage important e-commerce operations such as customers, products, categories, suppliers, orders, payments, inventory, shipments, reviews, coupons, cart items, and wishlists.

The project focuses on database design, relationships between entities, data management, and SQL-based business analysis.

---

## 🛠️ Technologies Used

* **Database:** MySQL 8.0
* **Query Language:** SQL
* **Data Generation:** Python
* **Python Library:** Faker
* **Database Tool:** MySQL Workbench

---

## 🗄️ Database Features

The database contains multiple related tables for managing:

* 👤 Customers
* 🏠 Customer Addresses
* 📦 Products
* 🗂️ Categories
* 🏭 Suppliers
* 🛒 Shopping Cart
* ❤️ Wishlist
* 📋 Orders
* 📦 Order Items
* 💳 Payments
* 🚚 Shipments
* 📊 Inventory
* ⭐ Product Reviews
* 🎟️ Coupons
* 🔄 Order Status History
* 🔗 Product Categories

---

## 📊 Database Structure

The project contains **16+ relational tables** connected using primary keys and foreign keys.

The database uses relational concepts such as:

* Primary Keys
* Foreign Keys
* Unique Constraints
* NOT NULL Constraints
* CHECK Constraints
* DEFAULT Values
* AUTO_INCREMENT
* One-to-One Relationships
* One-to-Many Relationships
* Many-to-Many Relationships

---

## 🧪 Dataset

The project contains **1000+ records across multiple tables**.

Because manually creating a large dataset would be inefficient, **Python Faker** was used to generate realistic test data.

The Python script was designed to generate data while maintaining the required relationships between tables and avoiding foreign-key constraint issues.

### Data Generation

```text
Python → Faker → Generate Test Data → MySQL Database
```

The data-generation script is available in:

```text
data_generation/
└── generate_data.py
```

---

## 🔍 SQL Concepts Used

The project demonstrates practical SQL concepts including:

* SELECT
* INSERT
* UPDATE
* DELETE
* WHERE
* ORDER BY
* LIMIT
* OFFSET
* DISTINCT
* Aggregate Functions
* GROUP BY
* HAVING
* INNER JOIN
* LEFT JOIN
* RIGHT JOIN
* CROSS JOIN
* Subqueries
* UNION / UNION ALL
* String Functions
* Date Functions
* Conditional Expressions

The queries are based on practical e-commerce business requirements.

---

## 📈 Example Business Queries

Some examples of analysis performed using SQL:

* Find the top customers based on total spending
* Identify products and their categories
* Analyze order and payment information
* Find shipped and delivered orders
* Analyze inventory information
* Retrieve customer order history
* Analyze product reviews
* Identify products with low inventory
* Analyze sales and order information

More queries are available in:

```text
sql/
└── queries.sql
```

---

## 📁 Project Structure

```text
E-Commerce-SQL-Project/
│
├── README.md
│
├── Queries/
│   ├── Basic-Level-Querie.sql
│   └── Intermediate-Level-Queries.sql
|   └── Advance-Level-Queries.sql
│
├── data generation/
│   └── insert_data.py
|   └── test_mysql.py
│
├── Report/
|   └── E-commerce_Report.pdf
|
└── screenshots/
|   ├── ER_Diagram.png
|   ├── TableName & RowCount.png
|   └── Query_Results.png
|
|
└── DemoCSV/
    └── customers.csv

```

---

## ▶️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Arunachalam118204/E-Commerce-Database
```

### 2. Open MySQL Workbench

Open the following SQL file:

```text
sql/database.sql
```

### 3. Create the Database

Run the database and table creation statements.

```sql
CREATE DATABASE e_commerce;
USE e_commerce;
```

### 4. Generate/Insert Data

The dataset can be generated using the Python Faker script or imported using the provided SQL data.

### 5. Run SQL Queries

Open:

```text
sql/queries.sql
```

and execute the queries in MySQL Workbench.

---

## 📸 Project Screenshots

### ER Diagram

The ER diagram shows the relationships between the major entities in the e-commerce database.

### Database Tables

### Sample Query Results

---

## 🎯 Project Objective

The main objective of this project is to design and implement a structured relational database for an e-commerce application and use SQL to perform meaningful business data analysis.

The project also helped demonstrate practical experience with **database normalization, relational database design, constraints, foreign-key relationships, large datasets, and SQL queries**.

---

## 👨‍💻 Author

**Arunachalam M.**

BE Computer Science and Engineering

GitHub: https://github.com/Arunachalam118204/E-Commerce-Database

LinkedI: https://www.linkedin.com/in/arunachalam-murugan-0419192a2/
