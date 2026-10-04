import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.title("📦 Shelf-Life Tracker")

# Input form
st.sidebar.header("Enter Product Details")
product_name = st.sidebar.text_input("Product Name")
start_date = st.sidebar.date_input("Start Date (Manufacture Date)", datetime.today())
shelf_days = st.sidebar.number_input("Shelf Life (Days)", min_value=0, value=30)
shelf_weeks = st.sidebar.number_input("Shelf Life (Weeks)", min_value=0, value=0)
shelf_months = st.sidebar.number_input("Shelf Life (Months)", min_value=0, value=0)

# Calculate expiry date
expiry_date = start_date + timedelta(days=shelf_days + shelf_weeks*7 + shelf_months*30)

# Days remaining
days_remaining = (expiry_date - datetime.today().date()).days
weeks_remaining = days_remaining / 7
months_remaining = days_remaining / 30

# Progress percentage
total_days = shelf_days + shelf_weeks*7 + shelf_months*30
progress = 100 * max(0, min(1, days_remaining / total_days))

# Display results
st.subheader("📊 Shelf-Life Status")
st.write(f"**Product:** {product_name}")
st.write(f"**Start Date:** {start_date}")
st.write(f"**Expiry Date:** {expiry_date}")
st.write(f"**Days Remaining:** {days_remaining}")
st.write(f"**Weeks Remaining:** {weeks_remaining:.1f}")
st.write(f"**Months Remaining:** {months_remaining:.1f}")
st.write(f"**Shelf-Life Remaining (%):** {progress:.2f}%")

# Progress bar
st.progress(progress/100)

# Optional: Save entries
if "data" not in st.session_state:
    st.session_state["data"] = []

if st.sidebar.button("Add to Dashboard"):
    st.session_state["data"].append({
        "Product": product_name,
        "Start Date": start_date,
        "Expiry Date": expiry_date,
        "Days Remaining": days_remaining,
        "Weeks Remaining": round(weeks_remaining,1),
        "Months Remaining": round(months_remaining,1),
        "Progress (%)": round(progress,2)
    })

if st.session_state["data"]:
    st.subheader("📋 Dashboard")
    df = pd.DataFrame(st.session_state["data"])
    st.dataframe(df)
