from pathlib import Path
from sqlalchemy import text
from scripts.database import get_engine


def create_schema():
    engine = get_engine()

    sql_path = Path(__file__).resolve().parent.parent / "sql" / "create_tables.sql"

    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()

    if not sql.strip():
        raise ValueError("create_tables.sql is empty")

    with engine.begin() as conn:
        conn.execute(text(sql))

    print("✅ Schema created successfully")