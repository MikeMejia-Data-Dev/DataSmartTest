import pandas as pd


def normalize_product_code(df: pd.DataFrame):
    df["product_code"] = (
        df["product_code"]
        .astype(str)
        .str.strip()
        .str.upper()
    )
    return df


def transform_sales(df: pd.DataFrame):
    df = df.copy()

    # Clean product codes
    df["product_code"] = df["product_code"].astype(str).str.strip().str.upper()

    # Handle invalid prices (will be rejected later)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Gross revenue
    df["gross_revenue"] = df["quantity"] * df["unit_price"]

    # Net revenue placeholder (adjust later with returns)
    df["net_revenue"] = df["gross_revenue"]

    # Clean dates
    if "invoice_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    # Missing customers
    df["customer_id"] = df["customer_id"].fillna("UNKNOWN")
    df["identified"] = df["customer_id"] != "UNKNOWN"

    print(f"Transformed sales: {len(df)} rows")
    return df


def transform_returns(df: pd.DataFrame):
    df = df.copy()

    df["product_code"] = df["stock_code"].astype(str).str.strip().str.upper()

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    if "invoice_date" in df.columns:
        df["return_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    print(f"Transformed returns: {len(df)} rows")
    return df


def split_quality_issues_sales(df: pd.DataFrame):
    """Business rules validation"""
    
    valid = df[(df["quantity"] > 0) & (df["unit_price"] > 0)].copy()
    
    rejected = df[(df["quantity"] <= 0) | (df["unit_price"] <= 0)].copy()

    rejected["reason"] = "invalid quantity or price"

    return valid, rejected