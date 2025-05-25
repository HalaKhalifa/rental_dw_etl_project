import mysql.connector

db_config = {
    'user': 'root',
    'password': 'newroot',
    'unix_socket': "/tmp/mysql.sock",
    'database': 'rental_dw_star'
}

sql_commands = [
    "DELETE FROM fact_daily_inventory_per_film_per_store;",
    "DELETE FROM fact_monthly_payment_per_staff_per_rent;",
    "DELETE FROM dim_date;",
    "TRUNCATE TABLE fact_daily_inventory_per_film_per_store;",
    "TRUNCATE TABLE fact_monthly_payment_per_staff_per_rent;",
    "ALTER TABLE dim_date AUTO_INCREMENT = 1;",
    "DELETE FROM dim_film;",
    "DELETE FROM dim_rental;",
    "DELETE FROM dim_store;",
    "DELETE FROM dim_staff;"
]

# Connect and execute
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    for command in sql_commands:
        cursor.execute(command)
        print(f"Executed: {command.strip()}")

    connection.commit()
    print("✅ All SQL commands executed successfully.")

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
finally:
    try:
        cursor.close()
        connection.close()
    except NameError:
        pass
