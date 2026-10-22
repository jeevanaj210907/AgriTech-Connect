import streamlit as st
import pandas as pd

st.title("🥬 FarmDirect Marketplace")

st.subheader("Connecting Farmers Directly With Buyers")

st.write(
    "A platform where farmers can list their "
    "produce and buyers can compare prices."
)

if "products" not in st.session_state:
    st.session_state.products = [
        {
            "Product": "Tomato",
            "Price per kg (₹)": 24,
            "Location": "Udupi"
        },
        {
            "Product": "Banana",
            "Price per kg (₹)": 32,
            "Location": "Mangaluru"
        },
        {
            "Product": "Cucumber",
            "Price per kg (₹)": 20,
            "Location": "Puttur"
        }
    ]

st.header("🛒 Available Products")

df = pd.DataFrame(st.session_state.products)
st.dataframe(df, use_container_width=True)

st.header("🌱 Add Your Produce")

with st.form("add_product"):
    product = st.text_input("Product name")
    price = st.number_input(
        "Price per kg (₹)",
        min_value=1.0,
        value=20.0
    )
    location = st.text_input("Village or town")

    submitted = st.form_submit_button("Add Product")

if submitted:
    if product.strip() and location.strip():
        st.session_state.products.append({
            "Product": product,
            "Price per kg (₹)": price,
            "Location": location
        })
        st.success("Product added successfully!")
        st.rerun()
    else:
        st.warning("Enter the product name and location.")

st.info(
    "Demo only: prices are illustrative and "
    "must be verified against current market data."
)
