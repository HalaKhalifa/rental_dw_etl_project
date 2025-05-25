import pandas as pd
from etl.helpers import clean_merge

# -------------------------------
# DIMENSIONS
# -------------------------------

def transform_dim_date(payment_df, rental_df):
    """Create dim_date from payment and rental dates."""
    dates = pd.concat([
        payment_df["payment_date"].dt.date,
        rental_df["rental_date"].dt.date
    ]).drop_duplicates().to_frame(name="full_date")

    dates["full_date"] = pd.to_datetime(dates["full_date"])
    dates["day"] = dates["full_date"].dt.day
    dates["month"] = dates["full_date"].dt.month
    dates["year"] = dates["full_date"].dt.year
    dates["day_name"] = dates["full_date"].dt.day_name()
    dates["month_name"] = dates["full_date"].dt.month_name()
    dates["month_start"] = dates["full_date"].dt.to_period("M").dt.to_timestamp()

    return dates.drop_duplicates()


def transform_dim_staff(staff, store, address, city, country):
    staff_full = clean_merge(staff, store, on="store_id", suffixes=('', '_store'))
    staff_full = clean_merge(staff_full, address, left_on="address_id_store", right_on="address_id")
    staff_full = clean_merge(staff_full, city, on="city_id")
    staff_full = clean_merge(staff_full, country, on="country_id")

    staff_star = pd.DataFrame({
        "staff_id": staff_full["staff_id"],
        "full_name": staff_full["first_name"].fillna("Unknown") + " " + staff_full["last_name"].fillna("Staff"),
        "email": staff_full["email"].fillna("no_email@unknown.com"),
        "store_name": "Store " + staff_full["store_id"].astype(str),
        "store_address": staff_full["address"].fillna('Jenin-Camp'),
        "city": staff_full["city"].fillna('Jenin'),
        "country": staff_full["country"].fillna('Palestine'),
        "active": staff_full["active"].fillna(1)
    })

    return staff_star.drop_duplicates()


def transform_dim_rental(rental, customer, address, city, country):
    rental_full = clean_merge(rental, customer, on="customer_id")
    rental_full = clean_merge(rental_full, address, on="address_id")
    rental_full = clean_merge(rental_full, city, on="city_id")
    rental_full = clean_merge(rental_full, country, on="country_id")
    rental_full = rental_full.dropna(subset=["inventory_id"])

    rental_star = pd.DataFrame({
        "rental_id": rental_full["rental_id"],
        "inventory_id": rental_full["inventory_id"],
        "rental_date": rental_full["rental_date"].fillna(pd.Timestamp("2027-10-7")),
        "return_date": rental_full["return_date"].fillna(pd.Timestamp("2027-10-7")),
        "customer_full_name": rental_full["first_name"] + " " + rental_full["last_name"],
        "customer_email": rental_full["email"].fillna("no_email@unknown.com"),
        "customer_city": rental_full["city"].fillna('Jenin'),
        "customer_country": rental_full["country"].fillna('Palestine')
    })

    return rental_star.drop_duplicates()


def transform_dim_film(film, language, film_category, category):
    film_full = clean_merge(film, language, on="language_id")
    film_full = clean_merge(film_full, film_category, on="film_id")
    film_full = clean_merge(film_full, category, on="category_id", suffixes=('_lang', '_cat'))
    film_full = film_full.rename(columns={
        "name_lang": "language_name",
        "name_cat": "category"
    })
    film_full = film_full.dropna(subset=["film_id"])

    film_star = pd.DataFrame({
        "film_id": film_full["film_id"],
        "title": film_full["title"].fillna("Unknown"),
        "release_year": film_full["release_year"],
        "language_name": film_full["language_name"].fillna("Unknown"),
        "rental_duration": film_full["rental_duration"],
        "rental_rate": film_full["rental_rate"],
        "length": film_full["length"],
        "rating": film_full["rating"],
        "category": film_full["category"].fillna("Uncategorized")
    })

    return film_star.drop_duplicates()


def transform_dim_store(store, address, city, country, staff):
    store_full = clean_merge(store, address, on="address_id")
    store_full = clean_merge(store_full, city, on="city_id")
    store_full = clean_merge(store_full, country, on="country_id")
    store_full = clean_merge(store_full, staff, left_on="manager_staff_id", right_on="staff_id", suffixes=('', '_mgr'))

    store_star = pd.DataFrame({
        "store_id": store_full["store_id"],
        "store_name": "Store " + store_full["store_id"].astype(str),
        "address": store_full["address"].fillna('Jenin-Camp'),
        "city": store_full["city"].fillna('Jenin'),
        "country": store_full["country"].fillna('Palestine'),
        "manager_name": store_full["first_name"].fillna("Manager") + " " + store_full["last_name"].fillna("Unknown")
    })

    return store_star.drop_duplicates()

# -------------------------------
# FACTS
# -------------------------------

def transform_fact_monthly_payment(payment_df, dim_date_df):
    """Aggregate payments by staff, rental, month → link to date_id."""
    payment_df["month_start"] = payment_df["payment_date"].dt.to_period("M").dt.to_timestamp()

    dim_month_anchor = dim_date_df.groupby("month_start", as_index=False).agg(
        date_id=("date_id", "min")
    )

    payment_fact = payment_df.groupby(
        ["staff_id", "rental_id", "month_start"], as_index=False
    ).agg(total_payment=("amount", "sum"))

    payment_fact = payment_fact.merge(dim_month_anchor, on="month_start", how="left")

    fact_monthly = payment_fact[["date_id", "staff_id", "rental_id", "total_payment"]]
    return fact_monthly


def transform_fact_daily_inventory(rental_df, inventory_df, dim_date_df):
    """Simulate inventory availability by film + store per day."""
    rental_df["rental_date"] = pd.to_datetime(rental_df["rental_date"]).fillna(pd.Timestamp("2099-12-31"))
    rental_df["return_date"] = pd.to_datetime(rental_df["return_date"]).fillna(pd.Timestamp("2099-12-31"))
    dim_date_df["full_date"] = pd.to_datetime(dim_date_df["full_date"]).fillna(pd.Timestamp("2099-12-31"))

    inventory_base = inventory_df[["inventory_id", "film_id", "store_id"]]

    # Cross join dates x inventory
    date_inventory = dim_date_df.assign(key=1).merge(inventory_base.assign(key=1), on="key").drop("key", axis=1)

    inventory_with_rentals = pd.merge(
        date_inventory,
        rental_df[["inventory_id", "rental_date", "return_date"]],
        on="inventory_id",
        how="left"
    )

    inventory_with_rentals["is_rented"] = (
        (inventory_with_rentals["rental_date"] <= inventory_with_rentals["full_date"]) &
        (inventory_with_rentals["return_date"] > inventory_with_rentals["full_date"])
    ).fillna(False)

    available_inventory = inventory_with_rentals[~inventory_with_rentals["is_rented"]]

    available_inventory = available_inventory.rename(columns={
        "film_id": "film_id",
        "store_id": "store_id"
    })

    daily_inventory = available_inventory.groupby(
        ["date_id", "film_id", "store_id"], as_index=False
    ).agg(inventory_count=("inventory_id", "count"))

    return daily_inventory