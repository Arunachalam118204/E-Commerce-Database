-- create database E_COMMERCE;
-- use E_COMMERCE;

CREATE TABLE customers (
    customer_id     BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    phone           VARCHAR(15)  NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_customers_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    CONSTRAINT check_customers_phone_format CHECK (phone REGEXP '^[0-9+][0-9 ]{7,14}$')
);

CREATE TABLE products (
    product_id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    price           NUMERIC(10,2) NOT NULL,
    sku             VARCHAR(50)   NOT NULL UNIQUE,
    stock_quantity  INTEGER       NOT NULL DEFAULT 0,
    created_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_products_price_positive CHECK (price >= 0),
    CONSTRAINT check_products_stock_nonneg   CHECK (stock_quantity >= 0)
);

CREATE TABLE categories (
    category_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_category_id BIGINT,

    CONSTRAINT fk_categories_parent
        FOREIGN KEY (parent_category_id)
        REFERENCES categories(category_id)
        ON DELETE SET NULL
);

CREATE TABLE suppliers (
    supplier_id     BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(150) NOT NULL,
    contact_email   VARCHAR(150),
    phone           VARCHAR(15),
    address         VARCHAR(255)
);

CREATE TABLE coupons (
    coupon_id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    code                VARCHAR(30) NOT NULL UNIQUE,
    discount_type       VARCHAR(10) NOT NULL,
    discount_value      DECIMAL(10,2) NOT NULL,
    min_order_amount    DECIMAL(10,2) NOT NULL DEFAULT 0,
    valid_from          TIMESTAMP NOT NULL,
    valid_until         TIMESTAMP NOT NULL,
    usage_limit         INT NOT NULL DEFAULT 0,
    used_count          INT NOT NULL DEFAULT 0,

    CONSTRAINT chk_coupons_discount_type CHECK (discount_type IN ('PERCENT', 'FIXED')),

    CONSTRAINT chk_coupons_discount_value_positive CHECK (discount_value > 0),

    CONSTRAINT chk_coupons_percent_range
    CHECK (
            discount_type != 'PERCENT'
            OR (discount_value > 0 AND discount_value <= 100)
        ),
CONSTRAINT chk_coupons_valid_dates CHECK (valid_until > valid_from),

CONSTRAINT chk_coupons_used_within_limit CHECK (used_count <= usage_limit)
);

CREATE TABLE addresses (
    address_id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id     BIGINT NOT NULL,
    address_line1   VARCHAR(255) NOT NULL,
    city            VARCHAR(100) NOT NULL,
    state           VARCHAR(100) NOT NULL,
    postal_code     VARCHAR(10) NOT NULL,
    country         VARCHAR(100) NOT NULL DEFAULT 'India',
    is_default      BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_addresses_customer
        FOREIGN KEY (customer_id)REFERENCES customers(customer_id)
        ON DELETE CASCADE
);


CREATE TABLE product_categories (
    product_id      BIGINT NOT NULL,
    category_id     BIGINT NOT NULL,

    PRIMARY KEY (product_id, category_id),

    CONSTRAINT fk_pc_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_pc_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
        ON DELETE CASCADE
);

CREATE TABLE cart_items (
    cart_item_id    BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id     BIGINT NOT NULL,
    product_id      BIGINT NOT NULL,
    quantity        INT NOT NULL DEFAULT 1,
    added_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_cart_customer_product
        UNIQUE (customer_id, product_id),

    CONSTRAINT fk_cart_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_cart_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_cart_quantity_positive
        CHECK (quantity > 0)
);
CREATE TABLE orders (
    order_id        BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id     BIGINT NOT NULL,
    address_id      BIGINT,
    coupon_id       BIGINT,
    order_date      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status          VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    total_amount    DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_orders_address
        FOREIGN KEY (address_id)
        REFERENCES addresses(address_id)
        ON DELETE SET NULL,

    CONSTRAINT fk_orders_coupon
        FOREIGN KEY (coupon_id)
        REFERENCES coupons(coupon_id)
        ON DELETE SET NULL,

    CONSTRAINT chk_orders_status
        CHECK (status IN (
            'PENDING',
            'CONFIRMED',
            'SHIPPED',
            'DELIVERED',
            'CANCELLED',
            'RETURNED'
        )),

    CONSTRAINT chk_orders_total_nonneg
        CHECK (total_amount >= 0)
);

CREATE TABLE order_items (
    order_item_id   BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id        BIGINT NOT NULL,
    product_id      BIGINT NOT NULL,
    quantity        INT NOT NULL,
    unit_price      DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_oi_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_oi_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_oi_quantity_positive
        CHECK (quantity > 0),

    CONSTRAINT chk_oi_unit_price_nonneg
        CHECK (unit_price >= 0)
);

CREATE TABLE payments (
    payment_id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id        BIGINT NOT NULL,
    payment_method  VARCHAR(20) NOT NULL,
    amount          DECIMAL(12,2) NOT NULL,
    payment_status  VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    transaction_id  VARCHAR(100),
    paid_at         TIMESTAMP,

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_payments_method
        CHECK (payment_method IN ('UPI', 'CARD', 'NETBANKING', 'COD', 'WALLET')),

    CONSTRAINT chk_payments_status
        CHECK (payment_status IN ('PENDING', 'SUCCESS', 'FAILED', 'REFUNDED')),

    CONSTRAINT chk_payments_amount_positive
        CHECK (amount >= 0)
);

CREATE TABLE product_reviews (
    review_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id      BIGINT NOT NULL,
    customer_id     BIGINT NOT NULL,
    rating          SMALLINT NOT NULL,
    comment         TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reviews_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_reviews_rating_range
        CHECK (rating BETWEEN 1 AND 5),

    CONSTRAINT uq_reviews_product_customer
        UNIQUE (product_id, customer_id)
);

CREATE TABLE inventory (
    inventory_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    supplier_id BIGINT,
    warehouse_location VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_inventory_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
        ON DELETE SET NULL,

    CONSTRAINT chk_inventory_quantity_nonneg
        CHECK (quantity >= 0),

    CONSTRAINT uq_inventory_product_warehouse
        UNIQUE (product_id, warehouse_location)
);

CREATE TABLE shipments (
    shipment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    carrier VARCHAR(100) NOT NULL,
    tracking_number VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,

    CONSTRAINT fk_shipments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_shipments_status
        CHECK (
            status IN (
                'PENDING',
                'PACKED',
                'SHIPPED',
                'IN_TRANSIT',
                'DELIVERED',
                'RETURNED'
            )
        ),

    CONSTRAINT chk_shipments_dates
        CHECK (
            delivered_at IS NULL
            OR shipped_at IS NULL
            OR delivered_at >= shipped_at
        )
);

CREATE TABLE order_status_history (
    status_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100),

    CONSTRAINT fk_osh_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_osh_status
        CHECK (
            status IN (
                'PENDING',
                'CONFIRMED',
                'SHIPPED',
                'DELIVERED',
                'CANCELLED',
                'RETURNED'
            )
        )
);

CREATE TABLE wishlist (
    wishlist_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_wishlist_customer_product
        UNIQUE (customer_id, product_id),

    CONSTRAINT fk_wishlist_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_wishlist_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);

SELECT table_name,table_rows
FROM information_schema.tables
WHERE table_schema = DATABASE();
