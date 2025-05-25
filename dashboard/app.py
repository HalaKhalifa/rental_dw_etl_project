import streamlit as st
import pandas as pd
import plotly.express as px
from queries import (
    get_monthly_fact, get_inventory_fact,
    get_top_categories, get_avg_payment_per_staff,
    get_top_inventory_avg
) 
 
st.set_page_config(layout="wide", page_title="Rental Data Warehouse Dashboard")
st.title("🎬 Rental Data Warehouse Dashboard")

# Load data
monthly_df = get_monthly_fact()
inventory_df = get_inventory_fact()
category_df = get_top_categories()
avg_staff_df = get_avg_payment_per_staff()
avg_inv_df = get_top_inventory_avg()

# ----- KPI Cards -----
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${monthly_df['total_payment'].sum():,.2f}")
col2.metric("Total Rentals", f"{monthly_df['rental_id'].nunique():,}")
col3.metric("Total Films", f"{inventory_df['film_id'].nunique():,}")
col4.metric("Total Stores", f"{inventory_df['store_id'].nunique():,}")

# ----- Monthly Revenue by Staff -----
st.subheader("💰 Monthly Revenue by Staff")
fig1 = px.bar(monthly_df, x="month_name", y="total_payment", color="staff", barmode="group",
              title="Monthly Revenue by Staff")
st.plotly_chart(fig1, use_container_width=True)

# ----- Revenue by Store -----
st.subheader("🏬 Revenue by Store")
fig2 = px.bar(monthly_df.groupby("store_name").sum(numeric_only=True).reset_index(),
              x="store_name", y="total_payment", title="Total Revenue per Store")
st.plotly_chart(fig2, use_container_width=True)

# ----- Top Customers by Payment -----
st.subheader("👥 Top Customers")
top_customers = monthly_df.groupby("customer_full_name").sum(numeric_only=True).nlargest(5, "total_payment").reset_index()
fig3 = px.pie(top_customers, names="customer_full_name", values="total_payment", title="Top 5 Customers by Revenue")
st.plotly_chart(fig3, use_container_width=True)

# ----- Average Payment per Rental by Staff -----
st.subheader("💡 Average Payment per Rental by Staff")

fig4 = px.bar(
    avg_staff_df,
    x="staff",
    y="avg_payment_per_rental",
    title="Average Payment Collected Per Rental by Staff",
    text_auto=True
)
st.plotly_chart(fig4, use_container_width=True)

# ----- Inventory by Film & Store -----
st.subheader("🎞 Inventory Trend")
film = st.selectbox("Select Film", inventory_df["title"].unique())
store = st.selectbox("Select Store", inventory_df["store_name"].unique())

inv_filtered = inventory_df[(inventory_df["title"] == film) & (inventory_df["store_name"] == store)]
fig5 = px.line(inv_filtered, x="full_date", y="inventory_count", title=f"Inventory of '{film}' in {store}")
st.plotly_chart(fig5, use_container_width=True)

# ----- Revenue by Category -----
st.subheader("🎬 Revenue by Film Category")
fig6 = px.bar(category_df, x="category", y="revenue", title="Top Categories by Revenue")
st.plotly_chart(fig6, use_container_width=True)

# ----- Most Stocked Films (Avg Inventory) -----
st.subheader("📦 Top 10 Films by Average Inventory Availability")

fig7 = px.bar(avg_inv_df, x="title", y="avg_inventory", title="Top 10 Films by Avg Available Inventory")
fig7.update_layout(xaxis_title="Film Title", yaxis_title="Average Inventory", xaxis_tickangle=45)
st.plotly_chart(fig7, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("📍 Built by Hala Khalifeh using Streamlit · Data Source: `rental_dw_star`")