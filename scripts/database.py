from sqlalchemy import create_engine
import os


def get_engine():
    user = os.getenv("DW_DB_USER")
    password = os.getenv("DW_DB_PASSWORD")
    host = os.getenv("DW_DB_HOST")
    port = os.getenv("DW_DB_PORT")
    database = os.getenv("DW_DB_NAME")

    url = (
        f"postgresql+psycopg2://"
        f"{user}:{password}@{host}:{port}/{database}"
    )

    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=3600,
        future=True,
    )