from sqlalchemy import create_engine
from config import engine_star

def load_table(df, table_name, if_exists="append"):
    """
    Load a DataFrame into the rental_dw_star database.
    Args:
        df (pd.DataFrame): The DataFrame to load.
        table_name (str): Target table name in star schema.
        if_exists (str): 'replace', 'append', or 'fail'
    """
    try:
        df.drop_duplicates(inplace=True)
        df.to_sql(table_name, engine_star, if_exists=if_exists, index=False)
        print(f"[LOAD] {len(df)} rows written to '{table_name}' ({if_exists}).")
    except Exception as e:
        print(f"[ERROR] Failed to load '{table_name}': {e}")