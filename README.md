# 🎬 Rental Data Warehouse Project

### Author: Hala Khalifeh  
**Course**: Data Warehouse – Second Semester 2024/2025  
**HW#2 & HW#3** – Star Schema + ETL + Dashboard

---

## 📌 Overview

This project implements a **complete data warehouse pipeline** for a film rental company using a **Star Schema**, Python-based ETL, and a Streamlit dashboard.

It covers:

- ✅ Star schema modeling
- ✅ ETL pipeline using Python & SQLAlchemy
- ✅ Handling missing & dirty data
- ✅ Interactive data visualization using Streamlit

---

## 🗂 Project Structure

```plaintext
rental_dw_etl_project/
├── dags/
│   └── rental_dw_etl_dag.py       # Airflow DAG (automated ETL)
├── etl/
│   ├── etl.py                     # Orchestration script (manual run)
│   ├── extract.py                 # Extract data from MySQL
│   ├── transform.py               # Build dimension & fact tables
│   ├── load.py                    # Load data into star schema
│   └── helpers.py                 # Shared utilities (e.g. clean_merge)
├── dashboard/
│   ├── queries.py                 # SQL queries for analysis
│   └── app.py                     # Streamlit dashboard UI
├── tests/
│   └── insert_test_data.sql       # Dirty data for testing ETL robustness
├── config.py                      # DB credentials (editable)
├── requirements.txt               # Dependencies
└── README.md                      # You're reading it!
```

---

## 🧠 Star Schema Design

### ✅ Fact Tables
- `fact_monthly_payment_per_staff_per_rent`
- `fact_daily_inventory_per_film_per_store`

### ✅ Dimension Tables
- `dim_date`
- `dim_staff`
- `dim_rental`
- `dim_film`
- `dim_store`

Design reference: [starSchemaDimensionalModel.pdf](./src/starSchemaDimensionalModel.pdf)

---

## ⚙️ ETL Pipeline

### 🔸 Extract

From the normalized database `rental_dw`:
```python
pd.read_sql_table("staff", engine_src)
```

### 🔸 Transform

- Join normalized tables
- Handle:
  - 🔹 Missing values (e.g., fill with `'Unknown'`, `2027-10-7`, `'Jenin'`)
  - 🔹 Redundant rows
- Generate dimensions & aggregates

### 🔸 Load

Push to `rental_dw_star` using `to_sql(if_exists="append")`.

Run manually:

```bash
python -m etl.etlPipline
```

---

## 🧪 Data Quality Testing

- Use `tests/insert_test_data.sql` to simulate dirty input
- ETL is built to handle:
  - NULLs in `email`, `return_date`, `language_id`
  - FK errors, out-of-range IDs, duplicate primary keys

Run test data:

```bash
mysql -u root -p rental_dw < tests/insert_test_data.sql
```

---

## 📊 Streamlit Dashboard

Located in `dashboard/app.py`, this interactive UI shows:

- 💰 Revenue by staff, store, and film category
- 🧮 Inventory levels over time
- 👥 Top customers
- 📆 Monthly performance
- 🔻 And more!

Run locally:

```bash
streamlit run dashboard/app.py
```

---

## 📦 Installation

Create a virtual environment and install:

```bash
pip install -r requirements.txt
```

Requirements include:
- `pandas`, `sqlalchemy`, `mysql-connector-python`
- `streamlit`, `plotly`
---

## ✅ Completed Tasks Checklist

- [x] Design star schema
- [x] Develop ETL with missing value handling
- [x] Modularize ETL code
- [x] Visualize data with Streamlit
- [x] Handle dirty test cases
- [x] Write documentation ✅

---

## 💡 Notes

- **Important**: Make sure to update the database connection information in `config.py` according to your environment (host, port, user, password, database).

- Set MySQL socket for macOS in `config.py`:
  ```python
  unix_socket="/tmp/mysql.sock"
  ```
---

## 👩🏻‍💻 Author

**Hala Khalifeh**  
AI Student  
An-Najah National University  
Data Warehouse – Spring 2024/2025

---