import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="FarmDirect | AgriTech Connect",
    page_icon="🌱",
    layout="wide"
)

# ---------------- LANGUAGE SELECTION ----------------

language = st.selectbox(
    "🌐 Select Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    ["English", "ಕನ್ನಡ"],
    key="language_selector"
)

# ---------------- TRANSLATIONS ----------------

translations = {
    "English": {
        "title": "🌱 FarmDirect Marketplace",
        "subtitle": "Connecting Farmers Directly With Buyers",
        "intro": (
            "Discover produce listings, compare prices across "
            "Karnataka markets, and publish your own farm produce."
        ),
        "vegetables": "🥬 Vegetables Available",
        "markets": "🏪 Markets Represented",
        "listings": "📦 Product Listings",
        "price_note": (
            "Prices are user-submitted listings, not verified "
            "live APMC prices."
        ),
        "explore": "🔎 Explore Vegetable Prices",
        "search": "Search vegetable",
        "search_hint": "Example: Tomato",
        "select_market": "Select APMC market",
        "all_markets": "All Markets",
        "no_results": (
            "No matching listings found. Try another search "
            "or publish a new listing below."
        ),
        "compare": "💰 Compare Prices Across Markets",
        "choose_vegetable": "Choose a vegetable",
        "highest": "Highest listed price",
        "lowest": "Lowest listed price",
        "no_products": "Add a listing to start comparing prices.",
        "chart": "📊 Vegetable Price Chart",
        "chart_hint": (
            "This chart compares prices submitted by users. "
            "It does not show verified live market prices."
        ),
        "add_produce": "🌾 List Your Produce",
        "vegetable": "Vegetable",
        "price": "Asking price (₹/kg)",
        "quantity": "Available quantity (kg)",
        "preferred_market": "Preferred APMC market",
        "location": "Village or farm location",
        "location_hint": "Enter your village or farm location",
        "publish": "➕ Publish Produce Listing",
        "enter_location": "Please enter your village or farm location.",
        "saved": "Your listing has been saved successfully!",
        "save_error": (
            "Could not save the listing. Please check your "
            "database permissions and try again."
        ),
        "load_error": (
            "Could not load products. Check your database "
            "table and permissions."
        ),
        "connection_error": (
            "Database connection failed. Please check "
            "your Streamlit Secrets settings."
        ),
        "footer": "Empowering Farmers Through Technology",
        "prototype": "FarmDirect Marketplace | Engineering Project",
        "table_vegetable": "Vegetable",
        "table_price": "Price (₹/kg)",
        "table_market": "APMC Market",
        "table_location": "Location",
        "table_quantity": "Quantity (kg)"
    },

    "ಕನ್ನಡ": {
        "title": "🌱 ಫಾರ್ಮ್‌ಡೈರೆಕ್ಟ್ ಮಾರುಕಟ್ಟೆ",
        "subtitle": "ರೈತರಿಂದ ನೇರವಾಗಿ ಖರೀದಿದಾರರಿಗೆ",
        "intro": (
            "ತರಕಾರಿಗಳ ಪಟ್ಟಿಯನ್ನು ನೋಡಿ, ಕರ್ನಾಟಕದ ಮಾರುಕಟ್ಟೆಗಳ "
            "ಬೆಲೆಗಳನ್ನು ಹೋಲಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಕೃಷಿ ಉತ್ಪನ್ನಗಳನ್ನು ಪ್ರಕಟಿಸಿ."
        ),
        "vegetables": "🥬 ಲಭ್ಯವಿರುವ ತರಕಾರಿಗಳು",
        "markets": "🏪 ಮಾರುಕಟ್ಟೆಗಳು",
        "listings": "📦 ಉತ್ಪನ್ನಗಳ ಪಟ್ಟಿಗಳು",
        "price_note": (
            "ಈ ಬೆಲೆಗಳನ್ನು ಬಳಕೆದಾರರು ನಮೂದಿಸಿದ್ದಾರೆ. ಇವು "
            "ಪರಿಶೀಲಿಸಿದ ನೈಜ APMC ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳಲ್ಲ."
        ),
        "explore": "🔎 ತರಕಾರಿ ಬೆಲೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ",
        "search": "ತರಕಾರಿಯನ್ನು ಹುಡುಕಿ",
        "search_hint": "ಉದಾಹರಣೆ: Tomato",
        "select_market": "APMC ಮಾರುಕಟ್ಟೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "all_markets": "ಎಲ್ಲಾ ಮಾರುಕಟ್ಟೆಗಳು",
        "no_results": (
            "ಹೊಂದಾಣಿಕೆಯ ಪಟ್ಟಿಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಬೇರೆ ಹುಡುಕಾಟ "
            "ಪ್ರಯತ್ನಿಸಿ ಅಥವಾ ಹೊಸ ಪಟ್ಟಿಯನ್ನು ಪ್ರಕಟಿಸಿ."
        ),
        "compare": "💰 ಮಾರುಕಟ್ಟೆಗಳ ಬೆಲೆಗಳನ್ನು ಹೋಲಿಸಿ",
        "choose_vegetable": "ತರಕಾರಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "highest": "ಅತ್ಯಧಿಕ ಪಟ್ಟಿ ಬೆಲೆ",
        "lowest": "ಕಡಿಮೆ ಪಟ್ಟಿ ಬೆಲೆ",
        "no_products": "ಬೆಲೆ ಹೋಲಿಸಲು ಮೊದಲು ಉತ್ಪನ್ನವನ್ನು ಸೇರಿಸಿ.",
        "chart": "📊 ತರಕಾರಿ ಬೆಲೆಗಳ ಚಾರ್ಟ್",
        "chart_hint": (
            "ಈ ಚಾರ್ಟ್ ಬಳಕೆದಾರರು ನಮೂದಿಸಿದ ಬೆಲೆಗಳನ್ನು ಹೋಲಿಸುತ್ತದೆ. "
            "ಇದು ಪರಿಶೀಲಿಸಿದ ನೈಜ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳನ್ನು ತೋರಿಸುವುದಿಲ್ಲ."
        ),
        "add_produce": "🌾 ನಿಮ್ಮ ಕೃಷಿ ಉತ್ಪನ್ನವನ್ನು ಪ್ರಕಟಿಸಿ",
        "vegetable": "ತರಕಾರಿ",
        "price": "ಬೆಲೆ (₹/ಕೆಜಿ)",
        "quantity": "ಲಭ್ಯವಿರುವ ಪ್ರಮಾಣ (ಕೆಜಿ)",
        "preferred_market": "ಆದ್ಯತೆಯ APMC ಮಾರುಕಟ್ಟೆ",
        "location": "ಗ್ರಾಮ ಅಥವಾ ಕೃಷಿ ಸ್ಥಳ",
        "location_hint": "ನಿಮ್ಮ ಗ್ರಾಮ ಅಥವಾ ಕೃಷಿ ಸ್ಥಳವನ್ನು ನಮೂದಿಸಿ",
        "publish": "➕ ಉತ್ಪನ್ನದ ಪಟ್ಟಿಯನ್ನು ಪ್ರಕಟಿಸಿ",
        "enter_location": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಗ್ರಾಮ ಅಥವಾ ಕೃಷಿ ಸ್ಥಳವನ್ನು ನಮೂದಿಸಿ.",
        "saved": "ನಿಮ್ಮ ಉತ್ಪನ್ನದ ಪಟ್ಟಿ ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!",
        "save_error": (
            "ಪಟ್ಟಿಯನ್ನು ಉಳಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಡೇಟಾಬೇಸ್ "
            "ಅನುಮತಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."
        ),
        "load_error": (
            "ಉತ್ಪನ್ನಗಳನ್ನು ಲೋಡ್ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. "
            "ಡೇಟಾಬೇಸ್ ಟೇಬಲ್ ಮತ್ತು ಅನುಮತಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ."
        ),
        "connection_error": (
            "ಡೇಟಾಬೇಸ್ ಸಂಪರ್ಕ ವಿಫಲವಾಗಿದೆ. Streamlit Secrets "
            "ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ."
        ),
        "footer": "ತಂತ್ರಜ್ಞಾನದ ಮೂಲಕ ರೈತರ ಸಬಲೀಕರಣ",
        "prototype": "ಫಾರ್ಮ್‌ಡೈರೆಕ್ಟ್ ಮಾರುಕಟ್ಟೆ | ಎಂಜಿನಿಯರಿಂಗ್ ಪ್ರಾಜೆಕ್ಟ್",
        "table_vegetable": "ತರಕಾರಿ",
        "table_price": "ಬೆಲೆ (₹/ಕೆಜಿ)",
        "table_market": "APMC ಮಾರುಕಟ್ಟೆ",
        "table_location": "ಸ್ಥಳ",
        "table_quantity": "ಪ್ರಮಾಣ (ಕೆಜಿ)"
    }
}

t = translations[language]

# ---------------- DATABASE CONNECTION ----------------

@st.cache_resource
def connect_database():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

try:
    supabase = connect_database()
except Exception:
    st.error(t["connection_error"])
    st.stop()


# ---------------- LOAD PRODUCTS ----------------

def load_products():
    response = (
        supabase.table("farm_products")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    products = response.data

    columns = [
        "Vegetable",
        "Price (₹/kg)",
        "APMC Market",
        "Location",
        "Quantity (kg)"
    ]

    if not products:
        return pd.DataFrame(columns=columns)

    df = pd.DataFrame(products)

    df = df.rename(columns={
        "vegetable": "Vegetable",
        "price": "Price (₹/kg)",
        "apmc_market": "APMC Market",
        "location": "Location",
        "quantity_kg": "Quantity (kg)"
    })

    return df


try:
    products_df = load_products()
except Exception:
    st.error(t["load_error"])
    st.stop()


# ---------------- HEADER ----------------

st.title(t["title"])

st.subheader(t["subtitle"])

st.write(t["intro"])

st.divider()


# ---------------- DASHBOARD ----------------

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

col1.metric(t["vegetables"], vegetable_count)
col2.metric(t["markets"], market_count)
col3.metric(t["listings"], total_listings)

st.caption(t["price_note"])

st.divider()


# ---------------- SEARCH AND FILTER ----------------

st.header(t["explore"])

filter1, filter2 = st.columns(2)

with filter1:
    search = st.text_input(
        t["search"],
        placeholder=t["search_hint"]
    )

with filter2:
    available_markets = sorted(
        products_df["APMC Market"].dropna().unique().tolist()
    )

    market_options = [t["all_markets"]] + available_markets

    selected_market = st.selectbox(
        t["select_market"],
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

if selected_market != t["all_markets"]:
    filtered_df = filtered_df[
        filtered_df["APMC Market"] == selected_market
    ]


# Translate table headings without changing database values

table_names = {
    "Vegetable": t["table_vegetable"],
    "Price (₹/kg)": t["table_price"],
    "APMC Market": t["table_market"],
    "Location": t["table_location"],
    "Quantity (kg)": t["table_quantity"]
}

if not filtered_df.empty:
    display_df = filtered_df.sort_values(
        "Price (₹/kg)",
        ascending=False
    ).rename(columns=table_names)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info(t["no_results"])

st.divider()


# ---------------- PRICE COMPARISON ----------------

st.header(t["compare"])

if not products_df.empty:

    vegetables = sorted(
        products_df["Vegetable"].dropna().unique().tolist()
    )

    selected_vegetable = st.selectbox(
        t["choose_vegetable"],
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
        t["highest"],
        f"₹{float(highest['Price (₹/kg)']):.2f}/kg",
        str(highest["APMC Market"])
    )

    col2.metric(
        t["lowest"],
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
        ].rename(columns=table_names),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(t["no_products"])

st.divider()


# ---------------- PRICE CHART ----------------

st.header(t["chart"])
st.caption(t["chart_hint"])

if not products_df.empty:

    chart_df = products_df[
        ["Vegetable", "Price (₹/kg)", "APMC Market"]
    ].copy()

    chart_df["Price (₹/kg)"] = pd.to_numeric(
        chart_df["Price (₹/kg)"],
        errors="coerce"
    )

    chart_df = chart_df.dropna(
        subset=["Price (₹/kg)"]
    )

    if not chart_df.empty:

        chart_df["Market / Vegetable"] = (
            chart_df["Vegetable"]
            + " - "
            + chart_df["APMC Market"]
        )

        chart_df = chart_df.set_index("Market / Vegetable")

        st.bar_chart(chart_df["Price (₹/kg)"])

    else:
        st.info(t["no_products"])

else:
    st.info(t["no_products"])

st.divider()


# ---------------- FARMER LISTING FORM ----------------

st.header(t["add_produce"])

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
            t["vegetable"],
            vegetable_names
        )

        new_price = st.number_input(
            t["price"],
            min_value=0.01,
            max_value=100000.0,
            value=20.0,
            step=1.0
        )

        new_quantity = st.number_input(
            t["quantity"],
            min_value=1,
            max_value=1000000,
            value=100,
            step=10
        )

    with col2:

        new_market = st.selectbox(
            t["preferred_market"],
            market_names
        )

        farmer_location = st.text_input(
            t["location"],
            placeholder=t["location_hint"]
        )

    submitted = st.form_submit_button(
        t["publish"],
        use_container_width=True
    )


if submitted:

    if not farmer_location.strip():

        st.error(t["enter_location"])

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
                f"{t['saved']} "
                f"({new_vegetable})"
            )

            st.rerun()

        except Exception:

            st.error(t["save_error"])


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    f"""
    <div style="text-align:center; padding:15px;">
        <h3>🌱 AgriTech Connect</h3>
        <p>{t["footer"]}</p>
        <p>{t["prototype"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)
