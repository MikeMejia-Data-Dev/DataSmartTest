import pandas as pd


# -----------------------------
# BASIC QUALITY CHECKS
# -----------------------------

def check_required_columns(df, required_cols):
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return True


def check_nulls(df, critical_columns):
    issues = {}

    for col in critical_columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            issues[col] = int(null_count)

    return issues


def check_negative_values(df, numeric_columns):
    issues = {}

    for col in numeric_columns:
        if col in df.columns:
            invalid = (df[col] <= 0).sum()
            if invalid > 0:
                issues[col] = int(invalid)

    return issues


def check_duplicates(df, subset_cols):
    duplicates = df.duplicated(subset=subset_cols).sum()
    return int(duplicates)


# -----------------------------
# SALES VALIDATION
# -----------------------------

def validate_sales(df: pd.DataFrame):
    print("🔍 Validating sales data...")

    required_cols = [
        "invoice_no",
        "product_code",
        "quantity",
        "unit_price",
        "customer_id"
    ]

    check_required_columns(df, required_cols)

    nulls = check_nulls(df, ["product_code", "quantity", "unit_price"])
    negatives = check_negative_values(df, ["quantity", "unit_price"])
    duplicates = check_duplicates(
        df,
        subset_cols=["invoice_no", "product_code", "customer_id"]
    )

    issues = {
        "nulls": nulls,
        "negatives": negatives,
        "duplicates": duplicates
    }

    print(f"Validation issues: {issues}")

    return df, issues


# -----------------------------
# RETURNS VALIDATION
# -----------------------------

def validate_returns(df: pd.DataFrame):
    print("🔍 Validating returns data...")

    required_cols = [
        "invoice_no",
        "product_code",
        "quantity"
    ]

    check_required_columns(df, required_cols)

    nulls = check_nulls(df, ["product_code", "quantity"])
    negatives = check_negative_values(df, ["quantity"])
    duplicates = check_duplicates(
        df,
        subset_cols=["invoice_no", "product_code"]
    )

    issues = {
        "nulls": nulls,
        "negatives": negatives,
        "duplicates": duplicates
    }

    print(f"Validation issues: {issues}")

    return df, issues


# -----------------------------
# PIPELINE DECISION LOGIC
# -----------------------------

def split_valid_invalid_sales(df: pd.DataFrame):
    """
    Business rules:
    - quantity <= 0 → invalid
    - unit_price <= 0 → invalid
    """

    valid = df[(df["quantity"] > 0) & (df["unit_price"] > 0)].copy()

    invalid = df[(df["quantity"] <= 0) | (df["unit_price"] <= 0)].copy()

    invalid["reason"] = "invalid quantity or unit_price"

    return valid, invalid


def split_valid_invalid_returns(df: pd.DataFrame):
    valid = df[df["quantity"] > 0].copy()

    invalid = df[df["quantity"] <= 0].copy()

    invalid["reason"] = "invalid return quantity"

    return valid, invalid