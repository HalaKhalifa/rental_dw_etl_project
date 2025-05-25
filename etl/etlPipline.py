from sqlalchemy import create_engine
from config import engine_star
import pandas as pd
from etl.extract import extract_all_tables
from etl.transform import (
    transform_dim_date, transform_dim_staff, transform_dim_rental,
    transform_dim_film, transform_dim_store,
    transform_fact_monthly_payment, transform_fact_daily_inventory
)
from etl.load import load_table

def run_etl():
    print("🚀 Starting ETL Process")
    
    # 1. Extract
    print("📥 Extracting source tables...")
    tables = extract_all_tables()

    # 2. Transform Dimensions
    print("🧱 Transforming dimension tables...")

    dim_date = transform_dim_date(tables["payment"], tables["rental"])
    load_table(dim_date, "dim_date")
    dim_date = pd.read_sql_table("dim_date", engine_star)

    dim_staff = transform_dim_staff(tables["staff"], tables["store"], tables["address"], tables["city"], tables["country"])
    load_table(dim_staff, "dim_staff")

    dim_rental = transform_dim_rental(tables["rental"], tables["customer"], tables["address"], tables["city"], tables["country"])
    load_table(dim_rental, "dim_rental")
    dim_rental = pd.read_sql_table("dim_rental", engine_star)

    dim_film = transform_dim_film(tables["film"], tables["language"], tables["film_category"], tables["category"])
    load_table(dim_film, "dim_film")

    dim_store = transform_dim_store(tables["store"], tables["address"], tables["city"], tables["country"], tables["staff"])
    load_table(dim_store, "dim_store")

    # 3. Transform Fact Tables
    print("📊 Transforming fact tables...")

    fact_monthly = transform_fact_monthly_payment(tables["payment"], dim_date)
    load_table(fact_monthly, "fact_monthly_payment_per_staff_per_rent")

    fact_daily_inventory = transform_fact_daily_inventory(dim_rental, tables["inventory"], dim_date)
    load_table(fact_daily_inventory, "fact_daily_inventory_per_film_per_store")

    print("✅ ETL process completed successfully!")
    
if __name__ == "__main__":
    run_etl()
