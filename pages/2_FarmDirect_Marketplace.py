import streamlit as st
import pandas as pd

st.set_page_config(
page_title="FarmDirect Marketplace",
page_icon="🌱",
layout="wide"
)

st.title("🌱 FarmDirect Marketplace")
st.subheader("Connecting Farmers Directly With Buyers")

st.markdown(
"Discover fresh produce, compare prices, and support local farmers."
)

Initialize product data

if "products" not in st.session_state:
st.session_state.products = [
{"Product": "Tomato", "Price per kg (₹)": 24.0, "Location": "Udupi"},
{"Product": "Banana", "Price per kg (₹)": 32.0, "Location": "Mangaluru"},
{"Product": "Cucumber", "Price per kg (₹)": 20.0, "Location": "Puttur"},
{"Product": "Onion", "Price per kg (₹)": 25.0, "Location": "Bengaluru"},
{"Product": "Potato", "Price per kg (₹)": 28.0, "Location": "Udupi"}
]

st.divider()

Marketplace

st.header("🛒 Explore Available Produce")

products = st.session_state.products
df = pd.DataFrame(products)

Summary metrics

col1, col2 = st.columns(2)

with col1:
st.metric("Available Listings", len(df))

with col2:
if not df.empty:
st.metric("Average Price per kg", f"₹{df['Price per kg (₹)'].mean():.2f}")
else:
st.metric("Average Price per kg", "₹0.00")

st.divider()

Search and filters

search_col, location_col, sort_col = st.columns(3)

with search_col:
search = st.text_input("🔍 Search produce", placeholder="e.g. Tomato")

with location_col:
locations = ["All Locations"] + sorted(
df["Location"].unique().tolist()
)
selected_location = st.selectbox("📍 Choose location", locations)

with sort_col:
sort_order = st.selectbox(
"💰 Sort by price",
["Default", "Lowest to Highest", "Highest to Lowest"]
)

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

if sort_order == "Lowest to Highest":
filtered_df = filtered_df.sort_values("Price per kg (₹)")

elif sort_order == "Highest to Lowest":
filtered_df = filtered_df.sort_values(
"Price per kg (₹)", ascending=False
)

if filtered_df.empty:
st.warning("No matching products found. Try different filters.")
else:
st.dataframe(
filtered_df.reset_index(drop=True),
use_container_width=True,
hide_index=True
)

st.divider()

Add produce

st.header("🌾 Sell Your Produce")
st.write("Farmers can add their produce to the marketplace below.")

with st.form("add_product", clear_on_submit=True):
product = st.text_input("Product name")
price = st.number_input(
"Price per kg (₹)",
min_value=1.0,
max_value=100000.0,
value=20.0,
step=1.0
)
location = st.text_input("Village or town")

submitted = st.form_submit_button(
    "➕ Add Product",
    use_container_width=True
)

if submitted:
if not product.strip() or not location.strip():
st.error("Please enter both the product name and location.")
else:
st.session_state.products.append({
"Product": product.strip().title(),
"Price per kg (₹)": price,
"Location": location.strip().title()
})
st.success(f"{product.strip().title()} added successfully!")
st.rerun()

st.divider()

Remove produce

st.header("🗑️ Manage Listings")

if st.session_state.products:
product_options = [
f"{i + 1}. {item['Product']} — ₹{item['Price per kg (₹)']:.2f}/kg ({item['Location']})"
for i, item in enumerate(st.session_state.products)
]

selected_product = st.selectbox(
    "Select a listing to remove",
    product_options
)

if st.button("Remove Selected Listing"):
    selected_index = product_options.index(selected_product)
    removed_product = st.session_state.products.pop(selected_index)
    st.success(f"{removed_product['Product']} listing removed.")
    st.rerun()

st.divider()

st.caption(
"🌱 FarmDirect Marketplace | Educational hackathon prototype. "
"Prices are illustrative and should be verified against current market rates."
)
