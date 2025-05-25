from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mysql+mysqlconnector://root:newroot@localhost/rental_dw_star?unix_socket=/tmp/mysql.sock")

def get_monthly_fact():
    return pd.read_sql("""
        SELECT f.*, d.year, d.month, d.month_name, s.full_name AS staff, t.store_name,
               r.customer_full_name, r.customer_country, r.customer_city
        FROM fact_monthly_payment_per_staff_per_rent f
        JOIN dim_date d ON f.date_id = d.date_id
        JOIN dim_staff s ON f.staff_id = s.staff_id
        JOIN dim_rental r ON f.rental_id = r.rental_id
        JOIN dim_store t ON s.store_name = t.store_name
    """, engine)

def get_inventory_fact():
    return pd.read_sql("""
        SELECT f.*, d.full_date, s.title, t.store_name
        FROM fact_daily_inventory_per_film_per_store f
        JOIN dim_date d ON f.date_id = d.date_id
        JOIN dim_film s ON f.film_id = s.film_id
        JOIN dim_store t ON f.store_id = t.store_id
    """, engine)

def get_top_categories():
    return pd.read_sql("""
        SELECT s.category, SUM(f.total_payment) AS revenue
        FROM fact_monthly_payment_per_staff_per_rent f
        JOIN dim_rental r ON f.rental_id = r.rental_id
        JOIN dim_film s ON r.inventory_id = s.film_id
        GROUP BY s.category ORDER BY revenue DESC LIMIT 10
    """, engine)

def get_avg_payment_per_staff():
    return pd.read_sql("""
        SELECT s.full_name AS staff, COUNT(f.rental_id) AS rental_count,
               SUM(f.total_payment) AS total_revenue,
               ROUND(SUM(f.total_payment) / COUNT(f.rental_id), 2) AS avg_payment_per_rental
        FROM fact_monthly_payment_per_staff_per_rent f
        JOIN dim_staff s ON f.staff_id = s.staff_id
        GROUP BY s.full_name
        ORDER BY avg_payment_per_rental DESC
    """, engine)


def get_top_inventory_avg():
    return pd.read_sql("""
        SELECT f.title, ROUND(AVG(fi.inventory_count), 2) AS avg_inventory
        FROM fact_daily_inventory_per_film_per_store fi
        JOIN dim_film f ON fi.film_id = f.film_id
        GROUP BY f.title
        ORDER BY avg_inventory DESC
        LIMIT 10
    """, engine)
