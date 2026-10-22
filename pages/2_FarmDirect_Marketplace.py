import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FarmDirect Marketplace",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 FarmDirect Marketplace")

st.subheader("Connecting Farmers Directly With Buyers")

st.write(
    "Farmers can list their products, set prices, "
    "and help buyers compare local market prices."
)

# Store products
if "products" not in st.session_state:
    st.session_state["products"] = [
        {
            "Product": "Tomato",
            "Price per kg (₹)": 24.0,
            "Location": "Udupi"
        },
        {
            "Product": "Banana",
            "Price per kg (₹)": 32.0,
            "Location": "Mangaluru"
        },
        {
            "Product": "Cucumber",
            "Price per kg (₹)": 20.0,
            "Location": "Puttur"
        }
    ]

# Available products
st.header("🛒 Available Products")

df = pd.DataFrame(st.session_state["products"])

search = st.text_input("🔍 Search for a product")

if search:
    df = df[
        df["Product"].str.contains(
            search, case=False, na=False
        )
    ]

if len(df) > 0:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No matching products found.")

# Add products
st.header("🌾 Add Your Produce")

with st.form("product_form"):
    product = st.text_input("Product name")

    price = st.number_input(
        "Price per kg (₹)",
        min_value=1.0,
        max_value=100000.0,
        value=20.0
    )

    location = st.text_input("Village or town")

    submit = st.form_submit_button("➕ Add Product")

if submit:
    if product.strip() and location.strip():
        new_product = {
            "Product": product.strip(),
            "Price per kg (₹)": price,
            "Location": location.strip()
        }

        st.session_state["products"].append(new_product)

        st.success("Product added successfully!")
        st.rerun()

    else:
        st.error("Please enter both product name and location.")

st.divider()

st.info(
    "Educational prototype: Prices are sample values "
    "and are not verified live market prices."
)

st.caption("AgriTech Connect | FarmDirect Marketplace")
