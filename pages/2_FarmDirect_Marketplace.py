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

Search by product name

search = st.text_input("🔍 Search products")

Filter by location

locations = ["All Locations"] + sorted(
df["Location"].unique().tolist()
)
selected_location = st.selectbox(
"📍 Filter by Location",
locations
)

Apply filters

filtered_df = df.copy()

if search.strip():
filtered_df = filtered_df[
filtered_df["Product"].str.contains(
search.strip(), case=False, na=False
)
]

if selected_location != "All Locations":
filtered_df = filtered_df[
filtered_df["Location"] == selected_location
]

Display results

if not filtered_df.empty:
st.dataframe(filtered_df, use_container_width=True)
st.success(f"{len(filtered_df)} product(s) found.")
else:
st.warning("No products found. Try another search.")

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
