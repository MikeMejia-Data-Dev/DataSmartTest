# 📊 Retail Data Engineering Pipeline (Airflow + PostgreSQL)

## 🚀 Overview

This project implements an end-to-end data engineering pipeline using Apache Airflow, Docker, and PostgreSQL.
It ingests raw retail datasets (Kaggle CSVs), processes them through an ETL workflow, validates data quality, and loads structured data into a relational data warehouse.

The system is fully containerized and runs with a single command:

```bash
docker compose up
```

## 🧱 Architecture
  Kaggle CSVs
         │
         ▼
  Apache Airflow

  (Docker Orchestration)

│

┌──────────────────────────────────┐

│        ETL Pipeline              │

│                                  │

│  Extract → Transform → Validate  │

│            → Load                │

└──────────────────────────────────┘

│

▼

PostgreSQL Warehouse

│

▼

SQL Analytics Layer

## 🛠️ Tech Stack

- Apache Airflow 3.x
- Docker & Docker Compose
- PostgreSQL (Metadata + Data Warehouse)
- Python 3.10+
- Pandas
- SQLAlchemy
- Kaggle datasets (CSV ingestion)

## 📁 Project Structure
datamart-pipeline/

│

├── docker-compose.yml

├── .env

├── README.md

│

├── dags/

│   └── retail_pipeline.py

│

├── scripts/

│   ├── database.py

│   ├── init_db.py

│   ├── extract.py

│   ├── transform.py

│   └── validate.py

│

├── sql/

│   └── create_tables.sql

│

├── data/

│   └── raw/

│       ├── data.csv

│       └── online_retail_II.csv

│

├── logs/

└── config/

## ⚙️ ETL Pipeline Design

The pipeline is structured into modular stages:

### 1. Extract
- Loads raw CSV datasets from Kaggle
- Standardizes initial structure
- Adds source tracking

### 2. Transform
- Cleans product codes
- Converts data types
- Computes:
  - `gross_revenue`
  - `net_revenue`
- Handles missing customer IDs

### 3. Validate
- Checks:
  - Null values
  - Negative quantities/prices
  - Duplicates
- Splits data into:
  - Valid records
  - Rejected records

### 4. Load
- Loads data into PostgreSQL warehouse:
  - `fact_sales`
  - `fact_returns`
  - `rejected_records`
  - Dimension tables

## 🗄️ Data Warehouse Schema

### Fact Tables
- `fact_sales`
- `fact_returns`

### Dimension Tables
- `dim_product`
- `dim_customer`
- `dim_date`

### Quality Table
- `rejected_records`

## 🧠 Business Rules

### Sales Rules
- `quantity <= 0` → rejected
- `unit_price <= 0` → rejected
- `gross_revenue = quantity * unit_price`

### Customer Handling
- Missing customers → `customer_id = NULL`
- Flagged as `identified = False`

### Product Normalization
- Uppercase product codes
- Trim whitespace

## 🔄 Airflow DAG

The main DAG: `retail_pipeline`

**Current tasks:**
- `create_schema`

**Future expansion:**
- `extract_sales`
- `extract_returns`
- `transform_sales`
- `validate_sales`
- `load_fact_sales`
- `load_fact_returns`
- `load_rejected_records`

## ▶️ How to Run

### 1. Start the project
```bash
docker compose up -d
```

### 2. Open Airflow UI
http://localhost:8080

### 3. Login
username: airflow

password: airflow

### 4. Trigger DAG
- Go to `retail_pipeline`
- Click **Trigger DAG**

## 🧪 Validate Database

Connect to PostgreSQL and check tables:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

## 📊 Example Business Queries

### Monthly Revenue
```sql
SELECT
    DATE_TRUNC('month', sale_date) AS month,
    SUM(net_revenue) AS revenue
FROM fact_sales
GROUP BY 1
ORDER BY 1;
```

### Top Products
```sql
SELECT
    product_code,
    SUM(net_revenue) AS revenue
FROM fact_sales
GROUP BY product_code
ORDER BY revenue DESC
LIMIT 10;
```

### Return Rate
```sql
SELECT
    product_code,
    SUM(quantity) AS returned_qty
FROM fact_returns
GROUP BY product_code;
```

## 🧩 Key Design Decisions

- Separation of ETL layers (Extract / Transform / Validate / Load)
- Idempotent schema creation (`CREATE TABLE IF NOT EXISTS`)
- Rejected records stored separately for auditing
- Modular Python architecture for scalability
- Airflow used only for orchestration (no business logic inside DAGs)

## 📌 Future Improvements

- Add staging (bronze/silver/gold layers)
- Add FastAPI data service
- Add dbt modeling layer
- Add data quality framework (Great Expectations)
- Add CI/CD pipeline for DAG testing

## 🏁 Summary

This project demonstrates a complete end-to-end data engineering system:

- Data ingestion (Kaggle CSVs)
- ETL pipeline (Airflow)
- Data validation layer
- Structured data warehouse
- SQL analytics layer
