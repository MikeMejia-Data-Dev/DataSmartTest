-- =========================
-- DIMENSIONS
-- =========================

CREATE TABLE IF NOT EXISTS dim_product (
    product_code TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id TEXT PRIMARY KEY,
    identified BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    week INT
);

-- =========================
-- FACT TABLES
-- =========================

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id SERIAL PRIMARY KEY,
    invoice_no TEXT,
    product_code TEXT,
    customer_id TEXT,
    country TEXT,
    quantity INT,
    unit_price NUMERIC(10,2),
    gross_revenue NUMERIC(12,2),
    net_revenue NUMERIC(12,2),
    sale_date TIMESTAMP,
    source TEXT
);

CREATE TABLE IF NOT EXISTS fact_returns (
    return_id SERIAL PRIMARY KEY,
    invoice_no TEXT,
    product_code TEXT,
    quantity INT,
    return_date TIMESTAMP,
    reason TEXT
);

-- =========================
-- QUALITY / REJECTED DATA
-- =========================

CREATE TABLE IF NOT EXISTS rejected_records (
    id SERIAL PRIMARY KEY,
    source TEXT,
    invoice_no TEXT,
    product_code TEXT,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);