from sqlalchemy import text


def load_dataframe(df, table_name, engine, if_exists="append"):
    if df.empty:
        print(f"⚠️ No data to load for {table_name}")
        return

    df.to_sql(
        table_name,
        engine,
        if_exists=if_exists,
        index=False,
        method="multi",
        chunksize=1000
    )

    print(f"Loaded {len(df)} rows into {table_name}")


def load_sales(df, engine):
    load_dataframe(df, "fact_sales", engine)


def load_returns(df, engine):
    load_dataframe(df, "fact_returns", engine)


def load_rejected(df, engine):
    load_dataframe(df, "rejected_records", engine)