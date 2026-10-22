import streamlit as st

st.title("🐟 AquaGuard AI")

st.subheader("Fish Pond Water Quality Monitor")

st.write(
    "Check water measurements and identify "
    "potential risks for fish farms."
)

ph = st.number_input(
    "Water pH",
    min_value=0.0,
    max_value=14.0,
    value=7.0
)

temperature = st.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=50.0,
    value=28.0
)

oxygen = st.number_input(
    "Dissolved Oxygen (mg/L)",
    min_value=0.0,
    max_value=30.0,
    value=6.0
)

if st.button("Check Water Quality"):

    problems = []

    if ph < 6.5 or ph > 8.5:
        problems.append("Check the water pH.")

    if temperature < 20 or temperature > 32:
        problems.append("Check the water temperature.")

    if oxygen < 5:
        problems.append("Dissolved oxygen is low.")

    if len(problems) >= 2:
        st.error("HIGH RISK: Check the pond promptly.")
    elif len(problems) == 1:
        st.warning("MEDIUM RISK: Review the reading.")
    else:
        st.success("No alerts from these basic checks.")

    for problem in problems:
        st.write("⚠️", problem)

st.caption(
    "Educational prototype. Thresholds require "
    "validation for the fish species and farm."
)
