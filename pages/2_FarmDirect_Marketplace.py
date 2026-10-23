import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="FarmDirect | AgriTech Connect",
    page_icon="🌱",
    layout="wide"
)
language = st.selectbox(
"🌐 Select Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
["English", "ಕನ್ನಡ"]
)


is_kannada = language == "ಕನ್ನಡ"


# Connect to Supabase
@st.cache_resource
def connect_database():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

try:
    supabase = connect_database()
except Exception:
    st.error(
        "Database connection failed. Please check "
        "your Streamlit Secrets settings."
    )
    st.stop()


# Load permanent listings
def load_products():
    response = (
        supabase.table("farm_products")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    products = response.data

    if not products:
        return pd.DataFrame(columns=[
            "Vegetable",
            "Price (₹/kg)",
            "APMC Market",
            "Location",
            "Quantity (kg)"
        ])

    df = pd.DataFrame(products)

    return df.rename(columns={
        "vegetable": "Vegetable",
        "price": "Price (₹/kg)",
        "apmc_market": "APMC Market",
        "location": "Location",
        "quantity_kg": "Quantity (kg)"
    })


try:
    products_df = load_products()
except Exception:
    st.error(
        "Could not load products. Check that the "
        "farm_products table and its permissions are correct."
    )
    st.stop()


# Header
st.title("🌱 FarmDirect Marketplace")

st.markdown("""
### Connecting Farmers Directly With Buyers

Discover produce listings, compare prices across Karnataka
markets, and publish your own farm produce.
""")

st.divider()


# Dashboard
total_listings = len(products_df)

vegetable_count = (
    products_df["Vegetable"].nunique()
    if total_listings else 0
)

market_count = (
    products_df["APMC Market"].nunique()
    if total_listings else 0
)

col1, col2, col3 = st.columns(3)

col1.metric("🥬 Vegetables Available", vegetable_count)
col2.metric("🏪 Markets Represented", market_count)
col3.metric("📦 Product Listings", total_listings)

st.caption(
    "Prices are user-submitted listings, not verified live APMC prices."
)

st.divider()


# Search and filters
st.header("🔎 Explore Vegetable Prices")

filter1, filter2 = st.columns(2)

with filter1:
    search = st.text_input(
        "Search vegetable",
        placeholder="Example: Tomato"
    )

with filter2:
    market_options = ["All Markets"] + sorted(
        products_df["APMC Market"].dropna().unique().tolist()
    )

    selected_market = st.selectbox(
        "Select APMC market",
        market_options
    )

filtered_df = products_df.copy()

if search.strip():
    filtered_df = filtered_df[
        filtered_df["Vegetable"].str.contains(
            search.strip(),
            case=False,
            na=False
        )
    ]

if selected_market != "All Markets":
    filtered_df = filtered_df[
        filtered_df["APMC Market"] == selected_market
    ]

if not filtered_df.empty:
    st.dataframe(
        filtered_df.sort_values(
            "Price (₹/kg)",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info(
        "No matching listings found. Try another search "
        "or publish a new listing below."
    )

st.divider()


# Price comparison
st.header("💰 Compare Prices Across Markets")

if not products_df.empty:
    vegetables = sorted(
        products_df["Vegetable"].dropna().unique().tolist()
    )

    selected_vegetable = st.selectbox(
        "Choose a vegetable",
        vegetables,
        key="price_comparison_vegetable"
    )

    comparison_df = products_df[
        products_df["Vegetable"] == selected_vegetable
    ].copy()

    comparison_df = comparison_df.sort_values(
        "Price (₹/kg)",
        ascending=False
    )

    highest = comparison_df.iloc[0]
    lowest = comparison_df.iloc[-1]

    col1, col2 = st.columns(2)

    col1.metric(
        "Highest listed price",
        f"₹{float(highest['Price (₹/kg)']):.2f}/kg",
        str(highest["APMC Market"])
    )

    col2.metric(
        "Lowest listed price",
        f"₹{float(lowest['Price (₹/kg)']):.2f}/kg",
        str(lowest["APMC Market"])
    )

    st.dataframe(
        comparison_df[
            [
                "Vegetable",
                "Price (₹/kg)",
                "APMC Market",
                "Location",
                "Quantity (kg)"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Add a listing to start comparing prices.")

st.divider()


# Add new listing
st.header("🌾 List Your Produce")

market_names = [
    "Bengaluru",
    "Mysuru",
    "Hubballi",
    "Belagavi",
    "Shivamogga",
    "Davanagere",
    "Mangaluru",
    "Udupi",
    "Kolar",
    "Hassan",
    "Puttur"
]

vegetable_names = [
    "Tomato",
    "Onion",
    "Potato",
    "Carrot",
    "Cabbage",
    "Cauliflower",
    "Beans",
    "Brinjal",
    "Green Chilli",
    "Cucumber",
    "Pumpkin",
    "Other"
]

with st.form("farmer_listing_form"):
    col1, col2 = st.columns(2)

    with col1:
        new_vegetable = st.selectbox(
            "Vegetable",
            vegetable_names
        )

        new_price = st.number_input(
            "Asking price (₹/kg)",
            min_value=0.01,
            max_value=100000.0,
            value=20.0,
            step=1.0
        )

        new_quantity = st.number_input(
            "Available quantity (kg)",
            min_value=1,
            max_value=1000000,
            value=100,
            step=10
        )

    with col2:
        new_market = st.selectbox(
            "Preferred APMC market",
            market_names
        )

        farmer_location = st.text_input(
            "Village or farm location"
        )

    submitted = st.form_submit_button(
        "➕ Publish Produce Listing",
        use_container_width=True
    )

if submitted:
    if not farmer_location.strip():
        st.error("Please enter your village or farm location.")
    else:
        new_listing = {
            "vegetable": new_vegetable,
            "price": float(new_price),
            "apmc_market": new_market,
            "location": farmer_location.strip(),
            "quantity_kg": int(new_quantity)
        }

        try:
            supabase.table("farm_products").insert(
                new_listing
            ).execute()

            st.success(
                f"Your {new_vegetable} listing has been saved!"
            )
            st.rerun()

        except Exception:
            st.error(
                "Could not save the listing. Please check "
                "your database permissions and try again."
            )


st.divider()

st.markdown("""
<div style="text-align:center; padding:12px;">
    <h4>🌱 AgriTech Connect</h4>
    <p>Empowering Farmers Through Technology</p>
    <p>FarmDirect Marketplace | Engineering Hackathon Prototype</p>
</div>
""", unsafe_allow_html=True)



            
