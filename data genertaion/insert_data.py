import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# ==========================================================
# MYSQL CONFIGURATION
# ==========================================================

HOST = "localhost"
USER = "root"
PASSWORD = "****"
DATABASE = "e_commerce"

# ==========================================================
# DATA COUNTS
# ==========================================================

CUSTOMER_COUNT = 1200
PRODUCT_COUNT = 1200
CATEGORY_COUNT = 1000
SUPPLIER_COUNT = 1000
COUPON_COUNT = 1000
ADDRESS_COUNT = 1500
PRODUCT_CATEGORY_COUNT = 2500
CART_COUNT = 1500
ORDER_COUNT = 1200
ORDER_ITEM_COUNT = 3000
PAYMENT_COUNT = 1500
REVIEW_COUNT = 1200
INVENTORY_COUNT = 1500
SHIPMENT_COUNT = 1200
HISTORY_COUNT = 4000
WISHLIST_COUNT = 1800

fake = Faker("en_IN")

random.seed(10)
Faker.seed(10)


# ==========================================================
# CONNECTION
# ==========================================================

def connect_database():

    print("Connecting to MySQL...")

    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

    print("Connected successfully!\n")

    return connection


# ==========================================================
# DATE GENERATOR
# ==========================================================

def random_date():

    return datetime.now() - timedelta(
        days=random.randint(0, 700),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
def get_ids(cursor, table_name, id_column):

    cursor.execute(
        f"SELECT {id_column} FROM {table_name}"
    )

    return [row[0] for row in cursor.fetchall()]


# ==========================================================
# BATCH INSERT
# ==========================================================

def insert_batch(cursor, sql, data):

    batch_size = 500

    for i in range(0, len(data), batch_size):

        batch = data[i:i + batch_size]

        cursor.executemany(sql, batch)

        print(
            f"    inserted {min(i + batch_size, len(data))}/{len(data)}"
        )


# ==========================================================
# 1. CUSTOMERS
# ==========================================================

def insert_customers(cursor):

    print("[1/16] Inserting customers...")

    data = []

    for i in range(1, CUSTOMER_COUNT + 1):

        first_name = fake.first_name()
        last_name = fake.last_name()

        # Remove special characters from names for email
        clean_first_name = "".join(
            c for c in first_name.lower()
            if c.isalnum()
        )

        clean_last_name = "".join(
            c for c in last_name.lower()
            if c.isalnum()
        )

        # Valid email format
        email = (
            f"{clean_first_name}."
            f"{clean_last_name}."
            f"{i}@example.com"
        )

        # Valid Indian phone number
        phone = "+91" + str(
            random.randint(6000000000, 9999999999)
        )

        password_hash = (
            "$2b$10$dummyhash" +
            str(i).zfill(20)
        )

        data.append((
            first_name[:50],
            last_name[:50],
            email[:150],
            phone,
            password_hash,
            random_date()
        ))

    sql = """
        INSERT INTO customers
        (
            first_name,
            last_name,
            email,
            phone,
            password_hash,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    insert_batch(cursor, sql, data)

    print("Customers completed.\n")

# ==========================================================
# 2. PRODUCTS
# ==========================================================

def insert_products(cursor):

    print("[2/16] Inserting products...")

    product_types = [
        "Laptop",
        "Keyboard",
        "Mouse",
        "Monitor",
        "Headphones",
        "Speaker",
        "Smart Watch",
        "Power Bank",
        "Webcam",
        "USB Cable",
        "Mobile Charger",
        "Gaming Chair",
        "Laptop Stand",
        "SSD",
        "Memory Card"
    ]

    data = []

    for i in range(1, PRODUCT_COUNT + 1):

        product_name = (
            random.choice(product_types)
            + " Model "
            + str(i)
        )

        price = round(
            random.uniform(100, 100000),
            2
        )

        sku = f"SKU{i:07d}"

        stock = random.randint(0, 500)

        data.append((
            product_name[:200],
            fake.text(max_nb_chars=200),
            price,
            sku,
            stock,
            random_date()
        ))

    sql = """
        INSERT INTO products
        (name, description, price, sku,
         stock_quantity, created_at)
        VALUES (%s,%s,%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Products completed.\n")


# ==========================================================
# 3. CATEGORIES
# ==========================================================

def insert_categories(cursor):

    print("[3/16] Inserting categories...")

    data = []

    parent_count = 50

    # Parent categories
    for i in range(1, parent_count + 1):

        data.append((
            f"Category {i}",
            None
        ))

    # Child categories
    for i in range(parent_count + 1, CATEGORY_COUNT + 1):

        parent_id = random.randint(
            1,
            parent_count
        )

        data.append((
            f"Category {i}",
            parent_id
        ))

    sql = """
        INSERT INTO categories
        (name, parent_category_id)
        VALUES (%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Categories completed.\n")


# ==========================================================
# 4. SUPPLIERS
# ==========================================================

def insert_suppliers(cursor):

    print("[4/16] Inserting suppliers...")

    data = []

    for i in range(1, SUPPLIER_COUNT + 1):

        data.append((
            f"Supplier Company {i}",
            f"supplier{i}@example.com",
            "+91" + str(
                random.randint(6000000000, 9999999999)
            ),
            fake.address().replace("\n", ", ")[:255]
        ))

    sql = """
        INSERT INTO suppliers
        (name, contact_email, phone, address)
        VALUES (%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Suppliers completed.\n")


# ==========================================================
# 5. COUPONS
# ==========================================================

def insert_coupons(cursor):

    print("[5/16] Inserting coupons...")

    data = []

    for i in range(1, COUPON_COUNT + 1):

        discount_type = random.choice([
            "PERCENT",
            "FIXED"
        ])

        if discount_type == "PERCENT":

            discount_value = round(
                random.uniform(5, 80),
                2
            )

        else:

            discount_value = round(
                random.uniform(50, 5000),
                2
            )

        valid_from = random_date()

        valid_until = (
            valid_from +
            timedelta(days=random.randint(10, 180))
        )

        usage_limit = random.randint(10, 1000)

        used_count = random.randint(
            0,
            usage_limit
        )

        data.append((
            f"COUPON{i:06d}",
            discount_type,
            discount_value,
            round(random.uniform(0, 5000), 2),
            valid_from,
            valid_until,
            usage_limit,
            used_count
        ))

    sql = """
        INSERT INTO coupons
        (code, discount_type, discount_value,
         min_order_amount, valid_from, valid_until,
         usage_limit, used_count)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Coupons completed.\n")


# ==========================================================
# 6. ADDRESSES
# ==========================================================

def insert_addresses(cursor):

    print("[6/16] Inserting addresses...")

    customer_ids = get_ids(
        cursor,
        "customers",
        "customer_id"
    )

    data = []

    for i in range(ADDRESS_COUNT):

        customer_id = random.choice(customer_ids)

        data.append((
            customer_id,
            fake.street_address()[:255],
            fake.city()[:100],
            fake.state()[:100],
            str(random.randint(100000, 999999)),
            "India",
            random.choice([0, 1])
        ))

    sql = """
        INSERT INTO addresses
        (
            customer_id,
            address_line1,
            city,
            state,
            postal_code,
            country,
            is_default
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Addresses completed.\n")


# ==========================================================
# 7. PRODUCT CATEGORIES
# ==========================================================

def insert_product_categories(cursor):

    print("[7/16] Inserting product_categories...")

    data = []

    used = set()

    while len(data) < PRODUCT_CATEGORY_COUNT:

        product_id = random.randint(
            1,
            PRODUCT_COUNT
        )

        category_id = random.randint(
            1,
            CATEGORY_COUNT
        )

        pair = (
            product_id,
            category_id
        )

        if pair not in used:

            used.add(pair)

            data.append(pair)

    sql = """
        INSERT INTO product_categories
        (product_id, category_id)
        VALUES (%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Product categories completed.\n")


# ==========================================================
# 8. CART ITEMS
# ==========================================================

def insert_cart_items(cursor):

    print("[8/16] Inserting cart_items...")

    data = []

    used = set()

    while len(data) < CART_COUNT:

        customer_id = random.randint(
            1,
            CUSTOMER_COUNT
        )

        product_id = random.randint(
            1,
            PRODUCT_COUNT
        )

        pair = (
            customer_id,
            product_id
        )

        if pair not in used:

            used.add(pair)

            data.append((
                customer_id,
                product_id,
                random.randint(1, 10),
                random_date()
            ))

    sql = """
        INSERT INTO cart_items
        (customer_id, product_id,
         quantity, added_at)
        VALUES (%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Cart items completed.\n")


# ==========================================================
# 9. ORDERS
# ==========================================================

def insert_orders(cursor):

    print("[9/16] Inserting orders...")

    statuses = [
        "PENDING",
        "CONFIRMED",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
        "RETURNED"
    ]

    data = []

    for i in range(ORDER_COUNT):

        customer_id = random.randint(
            1,
            CUSTOMER_COUNT
        )

        address_id = random.randint(
            1,
            ADDRESS_COUNT
        )

        coupon_id = (
            random.randint(1, COUPON_COUNT)
            if random.random() < 0.3
            else None
        )

        data.append((
            customer_id,
            address_id,
            coupon_id,
            random_date(),
            random.choice(statuses),
            round(
                random.uniform(100, 150000),
                2
            )
        ))

    sql = """
        INSERT INTO orders
        (customer_id, address_id, coupon_id,
         order_date, status, total_amount)
        VALUES (%s,%s,%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Orders completed.\n")


# ==========================================================
# 10. ORDER ITEMS
# ==========================================================

def insert_order_items(cursor):

    print("[10/16] Inserting order_items...")

    data = []

    for i in range(ORDER_ITEM_COUNT):

        order_id = random.randint(
            1,
            ORDER_COUNT
        )

        product_id = random.randint(
            1,
            PRODUCT_COUNT
        )

        quantity = random.randint(1, 10)

        unit_price = round(
            random.uniform(100, 100000),
            2
        )

        data.append((
            order_id,
            product_id,
            quantity,
            unit_price
        ))

    sql = """
        INSERT INTO order_items
        (order_id, product_id,
         quantity, unit_price)
        VALUES (%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Order items completed.\n")


# ==========================================================
# 11. PAYMENTS
# ==========================================================

def insert_payments(cursor):

    print("[11/16] Inserting payments...")

    methods = [
        "UPI",
        "CARD",
        "NETBANKING",
        "COD",
        "WALLET"
    ]

    statuses = [
        "PENDING",
        "SUCCESS",
        "FAILED",
        "REFUNDED"
    ]

    data = []

    for i in range(PAYMENT_COUNT):

        status = random.choice(statuses)

        transaction_id = None
        paid_at = None

        if status != "PENDING":

            transaction_id = (
                f"TXN{i + 1:012d}"
            )

        if status == "SUCCESS":

            paid_at = random_date()

        data.append((
            random.randint(1, ORDER_COUNT),
            random.choice(methods),
            round(
                random.uniform(100, 150000),
                2
            ),
            status,
            transaction_id,
            paid_at
        ))

    sql = """
        INSERT INTO payments
        (order_id, payment_method, amount,
         payment_status, transaction_id,
         paid_at)
        VALUES (%s,%s,%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Payments completed.\n")


# ==========================================================
# 12. REVIEWS
# ==========================================================

def insert_reviews(cursor):

    print("[12/16] Inserting product_reviews...")

    data = []

    used = set()

    while len(data) < REVIEW_COUNT:

        product_id = random.randint(
            1,
            PRODUCT_COUNT
        )

        customer_id = random.randint(
            1,
            CUSTOMER_COUNT
        )

        pair = (
            product_id,
            customer_id
        )

        if pair not in used:

            used.add(pair)

            data.append((
                product_id,
                customer_id,
                random.randint(1, 5),
                fake.text(max_nb_chars=200),
                random_date()
            ))

    sql = """
        INSERT INTO product_reviews
        (product_id, customer_id,
         rating, comment, created_at)
        VALUES (%s,%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Reviews completed.\n")


# ==========================================================
# 13. INVENTORY
# ==========================================================

def insert_inventory(cursor):

    print("[13/16] Inserting inventory...")

    warehouses = [
        "Chennai Warehouse",
        "Bangalore Warehouse",
        "Hyderabad Warehouse",
        "Mumbai Warehouse",
        "Delhi Warehouse",
        "Pune Warehouse",
        "Coimbatore Warehouse",
        "Trichy Warehouse"
    ]

    data = []

    used = set()

    while len(data) < INVENTORY_COUNT:

        product_id = random.randint(
            1,
            PRODUCT_COUNT
        )

        warehouse = random.choice(
            warehouses
        )

        pair = (
            product_id,
            warehouse
        )

        if pair not in used:

            used.add(pair)

            supplier_id = (
                random.randint(1, SUPPLIER_COUNT)
                if random.random() < 0.8
                else None
            )

            data.append((
                product_id,
                supplier_id,
                warehouse,
                random.randint(0, 500),
                random_date()
            ))

    sql = """
        INSERT INTO inventory
        (product_id, supplier_id,
         warehouse_location, quantity,
         last_updated)
        VALUES (%s,%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Inventory completed.\n")


# ==========================================================
# 14. SHIPMENTS
# ==========================================================

def insert_shipments(cursor):

    print("[14/16] Inserting shipments...")

    carriers = [
        "DHL",
        "FedEx",
        "BlueDart",
        "Delhivery",
        "DTDC",
        "Ekart"
    ]

    statuses = [
        "PENDING",
        "PACKED",
        "SHIPPED",
        "IN_TRANSIT",
        "DELIVERED",
        "RETURNED"
    ]

    data = []

    for i in range(SHIPMENT_COUNT):

        status = random.choice(statuses)

        shipped_at = None
        delivered_at = None
        tracking_number = None

        if status in [
            "SHIPPED",
            "IN_TRANSIT",
            "DELIVERED",
            "RETURNED"
        ]:

            shipped_at = random_date()

            tracking_number = (
                f"TRK{i + 1:012d}"
            )

        if status in [
            "DELIVERED",
            "RETURNED"
        ]:

            delivered_at = (
                shipped_at +
                timedelta(
                    days=random.randint(1, 10)
                )
            )

        data.append((
            random.randint(1, ORDER_COUNT),
            random.choice(carriers),
            tracking_number,
            status,
            shipped_at,
            delivered_at
        ))

    sql = """
        INSERT INTO shipments
        (order_id, carrier, tracking_number,
         status, shipped_at, delivered_at)
        VALUES (%s,%s,%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Shipments completed.\n")


# ==========================================================
# 15. STATUS HISTORY
# ==========================================================

def insert_status_history(cursor):

    print("[15/16] Inserting order_status_history...")

    statuses = [
        "PENDING",
        "CONFIRMED",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
        "RETURNED"
    ]

    users = [
        "system",
        "admin",
        "warehouse",
        "customer_service"
    ]

    data = []

    for i in range(HISTORY_COUNT):

        data.append((
            random.randint(1, ORDER_COUNT),
            random.choice(statuses),
            random_date(),
            random.choice(users)
        ))

    sql = """
        INSERT INTO order_status_history
        (order_id, status,
         changed_at, changed_by)
        VALUES (%s,%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Status history completed.\n")


# ==========================================================
# 16. WISHLIST
# ==========================================================

def insert_wishlist(cursor):

    print("[16/16] Inserting wishlist...")

    data = []

    used = set()

    while len(data) < WISHLIST_COUNT:

        customer_id = random.randint(
            1,
            CUSTOMER_COUNT
        )

        product_id = random.randint(
            1,
            PRODUCT_COUNT
        )

        pair = (
            customer_id,
            product_id
        )

        if pair not in used:

            used.add(pair)

            data.append((
                customer_id,
                product_id,
                random_date()
            ))

    sql = """
        INSERT INTO wishlist
        (customer_id, product_id, added_at)
        VALUES (%s,%s,%s)
    """

    insert_batch(cursor, sql, data)

    print("Wishlist completed.\n")


# ==========================================================
# MAIN
# ==========================================================

def main():

    connection = None

    try:

        connection = connect_database()

        cursor = connection.cursor()

       # insert_customers(cursor)
        #connection.commit()

        # insert_products(cursor)
        # connection.commit()

        # insert_categories(cursor)
        # connection.commit()

        # insert_suppliers(cursor)
        # connection.commit()

        # insert_coupons(cursor)
        # connection.commit()

        insert_addresses(cursor)
        connection.commit()

        insert_product_categories(cursor)
        connection.commit()

        insert_cart_items(cursor)
        connection.commit()

        insert_orders(cursor)
        connection.commit()

        insert_order_items(cursor)
        connection.commit()

        insert_payments(cursor)
        connection.commit()

        insert_reviews(cursor)
        connection.commit()

        insert_inventory(cursor)
        connection.commit()

        insert_shipments(cursor)
        connection.commit()

        insert_status_history(cursor)
        connection.commit()

        insert_wishlist(cursor)
        connection.commit()

        print("=" * 60)
        print("ALL DATA INSERTED SUCCESSFULLY!")
        print("=" * 60)

        cursor.close()
        connection.close()

    except Exception as e:

        print("\nERROR OCCURRED:")
        print(e)

        if connection:
            connection.rollback()
            connection.close()


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":
    main()