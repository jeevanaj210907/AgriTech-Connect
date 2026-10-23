import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FarmDirect | AgriTech Connect",
    page_icon="🌱",
    layout="wide"
)

# --------------------------------------------------
# PROFESSIONAL HEADER
# --------------------------------------------------

st.title("🌱 FarmDirect Marketplace")

st.markdown(
    """
    ### Connecting Farmers Directly With Buyers

    Compare vegetable prices across Karnataka markets,
    discover selling opportunities, and connect farmers
    with potential buyers.
    """
)

st.divider()

# --------------------------------------------------
# SAMPLE MARKET DATA
# Prices below are illustrative, not live APMC prices.
# --------------------------------------------------

if "products" not in st.session_state:

    st.session_state["products"] = [
        {
            "Vegetable": "Tomato",
            "Price (₹/kg)": 24.0,
            "APMC Market": "Kolar",
            "Location": "Kolar",
            "Quantity (kg)": 500
        },
        {
            "Vegetable": "Tomato",
            "Price (₹/kg)": 28.0,
            "APMC Market": "Bengaluru",
            "Location": "Bengaluru",
            "Quantity (kg)": 350
        },
        {
            "Vegetable": "Tomato",
            "Price (₹/kg)": 22.0,
            "APMC Market": "Mysuru",
            "Location": "Mysuru",
            "Quantity (kg)": 400
        },
        {
            "Vegetable": "Onion",
            "Price (₹/kg)": 30.0,
            "APMC Market": "Hubballi",
            "Location": "Hubballi",
            "Quantity (kg)": 600
        },
        {
            "Vegetable": "Onion",
            "Price (₹/kg)": 32.0,
            "APMC Market": "Belagavi",
            "Location": "Belagavi",
            "Quantity (kg)": 450
        },
        {
            "Vegetable": "Potato",
            "Price (₹/kg)": 25.0,
            "APMC Market": "Bengaluru",
            "Location": "Bengaluru",
            "Quantity (kg)": 500
        },
        {
            "Vegetable": "Potato",
            "Price (₹/kg)": 23.0,
            "APMC Market": "Davanagere",
            "Location": "Davanagere",
            "Quantity (kg)": 300
        },
        {
            "Vegetable": "Carrot",
            "Price (₹/kg)": 38.0,
            "APMC Market": "Kolar",
            "Location": "Kolar",
            "Quantity (kg)": 250
        },
        {
            "Vegetable": "Carrot",
            "Price (₹/kg)": 35.0,
            "APMC Market": "Mysuru",
            "Location": "Mysuru",
            "Quantity (kg)": 200
        },
        {
            "Vegetable": "Cabbage",
            "Price (₹/kg)": 18.0,
            "APMC Market": "Shivamogga",
            "Location": "Shivamogga",
            "Quantity (kg)": 400
        },
        {
            "Vegetable": "Cauliflower",
            "Price (₹/kg)": 32.0,
            "APMC Market": "Hassan",
            "Location": "Hassan",
            "Quantity (kg)": 250
        },
        {
            "Vegetable": "Beans",
            "Price (₹/kg)": 45.0,
            "APMC Market": "Mangaluru",
            "Location": "Mangaluru",
            "Quantity (kg)": 150
        },
        {
            "Vegetable": "Brinjal",
            "Price (₹/kg)": 26.0,
            "APMC Market": "Udupi",
            "Location": "Udupi",
            "Quantity (kg)": 300
        },
        {
            "Vegetable": "Green Chilli",
            "Price (₹/kg)": 40.0,
            "APMC Market": "Belagavi",
            "Location": "Belagavi",
            "Quantity (kg)": 200
        },
        {
            "Vegetable": "Cucumber",
            "Price (₹/kg)": 20.0,
            "APMC Market": "Puttur",
            "Location": "Puttur",
            "Quantity (kg)": 350
        },
        {
            "Vegetable": "Pumpkin",
            "Price (₹/kg)": 16.0,
            "APMC Market": "Davanagere",
            "Location": "Davanagere",
            "Quantity (kg)": 500
        },
        {
            "Vegetable": "Beans",
            "Price (₹/kg)": 48.0,
            "APMC Market": "Bengaluru",
            "Location": "Bengaluru",
            "Quantity (kg)": 180
        },
        {
            "Vegetable": "Brinjal",
            "Price (₹/kg)": 29.0,
            "APMC Market": "Mysuru",
            "Location": "Mysuru",
            "Quantity (kg)": 250
        },
        {
            "Vegetable": "Cabbage",
            "Price (₹/kg)": 21.0,
            "APMC Market": "Hassan",
            "Location": "Hassan",
            "Quantity (kg)": 320
        },
        {
            "Vegetable": "Green Chilli",
            "Price (₹/kg)": 43.0,
            "APMC Market": "Hubballi",
            "Location": "Hubballi",
            "Quantity (kg)": 220
        }
    ]

# --------------------------------------------------
# SUMMARY DASHBOARD
# --------------------------------------------------

products_df = pd.DataFrame(st.session_state["products"])

total_listings = len(products_df)

vegetable_count = (
    products_df["Vegetable"].nunique()
    if total_listings > 0 else 0
)

market_count = (
    products_df["APMC Market"].nunique()
    if total_listings > 0 else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "🥬 Vegetables Available",
    vegetable_count
)

col2.metric(
    "🏪 Markets Represented",
    market_count
)

col3.metric(
    "📦 Product Listings",
    total_listings
)

st.caption(
    "Demonstration data only. Prices are not verified live market quotations."
)

st.divider()

# --------------------------------------------------
# MARKET PRICE EXPLORER
# --------------------------------------------------

st.header("🔎 Explore Vegetable Prices")

filter1, filter2 = st.columns(2)

with filter1:
    search = st.text_input(
        "Search vegetable",
        placeholder="Example: Tomato"
    )

with filter2:
    market_options = ["All Markets"] + sorted(
        products_df["APMC Market"].unique().tolist()
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
    display_df = filtered_df.sort_values(
        "Price (₹/kg)",
        ascending=False
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No matching vegetables found.")

st.divider()

# --------------------------------------------------
# PRICE COMPARISON
# --------------------------------------------------

st.header("💰 Compare Prices Across Markets")

if not products_df.empty:

    vegetables = sorted(
        products_df["Vegetable"].unique().tolist()
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

    if not comparison_df.empty:

        best_price = comparison_df.iloc[0]
        lowest_price = comparison_df.iloc[-1]

        col1, col2 = st.columns(2)

        col1.metric(
            "Highest listed price",
            f"₹{best_price['Price (₹/kg)']:.2f}/kg",
            best_price["APMC Market"]
        )

        col2.metric(
            "Lowest listed price",
            f"₹{lowest_price['Price (₹/kg)']:.2f}/kg",
            lowest_price["APMC Market"]
        )

        st.subheader(
            f"{selected_vegetable}: Market Comparison"
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

        st.info(
            "Farmers should compare transport costs, market fees, "
            "quality requirements and expected selling prices before "
            "choosing a market. The highest listed price may not "
            "produce the highest net income."
        )

st.divider()

# --------------------------------------------------
# ADD FARMER LISTING
# --------------------------------------------------

st.header("🌾 List Your Produce")

st.write(
    "Add your vegetable, asking price, available quantity "
    "and preferred market."
)

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
            "Your asking price (₹/kg)",
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
            "Vegetable": new_vegetable,
            "Price (₹/kg)": float(new_price),
            "APMC Market": new_market,
            "Location": farmer_location.strip(),
            "Quantity (kg)": int(new_quantity)
        }

        st.session_state["products"].append(new_listing)

        st.success(
            f"Your {new_vegetable} listing has been added successfully!"
        )

        st.rerun()

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div style="text-align:center; padding:12px;">
        <h4>🌱 AgriTech Connect</h4>
        <p>Empowering Farmers Through Technology</p>
        <p>FarmDirect Marketplace | Engineering Hackathon Prototype</p>
    </div>
    """,
    unsafe_allow_html=True
)
