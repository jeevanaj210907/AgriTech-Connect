import streamlit as st
import numpy as np
import joblib
import os


st.set_page_config(
page_title="AquaGuard AI",
page_icon="🐟",
layout="wide"
)


st.title("🐟 AquaGuard AI")
st.subheader("Fish Pond Water Quality Monitor")


st.write(
"Enter your pond's water measurements to receive "
"an educational machine-learning risk classification."
)


Load the trained model


MODEL_PATH = os.path.join(
os.path.dirname(os.path.dirname(file)),
"aquaguard_model.pkl"
)


@st.cache_resource
def load_model():
return joblib.load(MODEL_PATH)


if not os.path.exists(MODEL_PATH):
st.error(
"The trained model file was not found. "
"Please complete the model training step first."
)
st.info(
"The training script must generate "
"aquaguard_model.pkl in the repository's root folder."
)
st.stop()


try:
model = load_model()
except Exception:
st.error(
"Could not load the model. Please check that "
"aquaguard_model.pkl was generated correctly."
)
st.stop()


st.divider()


st.header("Enter Water Measurements")


col1, col2 = st.columns(2)


with col1:
ph = st.number_input(
"Water pH",
min_value=0.0,
max_value=14.0,
value=7.0,
step=0.1
)


temperature = st.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=50.0,
    value=28.0,
    step=0.5
)



with col2:
oxygen = st.number_input(
"Dissolved Oxygen (mg/L)",
min_value=0.0,
max_value=30.0,
value=6.0,
step=0.1
)


ammonia = st.number_input(
    "Ammonia (mg/L)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=0.1
)



if st.button("🤖 Predict Water Quality Risk", use_container_width=True):


input_data = np.array([[
    ph,
    temperature,
    oxygen,
    ammonia
]])

prediction = model.predict(input_data)[0]

st.divider()
st.subheader("Prediction Result")

if prediction == "High Risk":
    st.error("🔴 HIGH RISK — Check the pond promptly.")

elif prediction == "Medium Risk":
    st.warning("🟠 MEDIUM RISK — Review the water measurements.")

else:
    st.success("🟢 LOW RISK — No risk identified by this model.")

st.write("**Model classification:**", prediction)

if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(input_data)[0]
    classes = model.classes_

    st.write("Model output scores:")
    st.bar_chart(
        {
            "Model score (%)": {
                str(label): round(float(probability) * 100, 2)
                for label, probability in zip(classes, probabilities)
            }
        }
    )



st.caption(
"Educational prototype only. This model uses synthetic "
"demonstration data and is not validated for real fish farms. "
"Its predictions and scores must not guide real pond-safety "
"decisions. Validate it with real, species-specific data first."
)


