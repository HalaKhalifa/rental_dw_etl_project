import pandas as pd
from config import engine_src

TABLE_NAMES = [
    "staff", "store", "address", "city", "country",
    "rental", "customer", "film", "language", "category",
    "film_category", "payment", "inventory"
]

def extract_table(table_name: str) -> pd.DataFrame:
    """Extract a single table from the source database."""
    try:
        df = pd.read_sql_table(table_name, engine_src)
        print(f"[EXTRACT] Loaded '{table_name}' with {len(df)} rows.")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to extract '{table_name}': {e}")
        return pd.DataFrame()

def extract_all_tables() -> dict:
    """Extract all relevant tables from the normalized rental_dw source DB."""
    extracted = {}
    for table in TABLE_NAMES:
        extracted[table] = extract_table(table)
    return extracted