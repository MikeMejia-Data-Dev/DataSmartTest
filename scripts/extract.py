import pandas as pd
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"

# Mapeo de columnas originales (estilo Kaggle) -> snake_case usado en todo el pipeline
SALES_COLUMN_MAP = {
    "Invoice": "invoice_no",
    "InvoiceNo": "invoice_no",       # algunas versiones del dataset usan este nombre
    "StockCode": "product_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "Price": "unit_price",           # versión "online_retail_II" usa "Price"
    "CustomerID": "customer_id",
    "Customer ID": "customer_id",    # variante con espacio
    "Country": "country",
}

RETURNS_COLUMN_MAP = {
    "Invoice": "invoice_no",
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "unit_price",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Customer ID": "customer_id",
    "Country": "country",
}


def _rename_columns(df: pd.DataFrame, column_map: dict) -> pd.DataFrame:
    """Renombra solo las columnas que existen en el DataFrame; ignora las que no aplican."""
    existing_map = {k: v for k, v in column_map.items() if k in df.columns}
    return df.rename(columns=existing_map)


def extract_sales():
    file_path = DATA_PATH / "data.csv"
    df = pd.read_csv(file_path, encoding="latin-1")
    df = _rename_columns(df, SALES_COLUMN_MAP)
    df["source"] = "sales"
    print(f"Extracted sales: {len(df)} rows, columns: {list(df.columns)}")
    return df


def extract_returns():
    file_path = DATA_PATH / "online_retail_II.xlsx"
    df = pd.read_excel(file_path)
    df = _rename_columns(df, RETURNS_COLUMN_MAP)
    df["source"] = "returns"
    print(f"Extracted returns: {len(df)} rows, columns: {list(df.columns)}")
    return df


def extract_all():
    sales = extract_sales()
    returns = extract_returns()
    return sales, returns