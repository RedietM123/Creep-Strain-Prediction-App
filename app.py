import streamlit as st
import joblib
import pandas as pd

# Load the trained model and preprocessing transformer

model = joblib.load('./models/xgboost_final_model_new.pkl')
transformer = joblib.load('./models/preprocessing_transformer_new.pkl')



# Title of the Web Application
st.title("Creep Strain Prediction App")

st.write(
    """
    This app predicts the **Creep Strain Value** based on concrete material properties and environmental conditions.
    """
)

# Sidebar for Input Features
st.sidebar.header("Input Features")


def get_user_input():
    cement_type = st.sidebar.selectbox("Cement Type", options=["rapid hardening cement", "Ordinary cement", "Type 1 Portland cement", "Shrinkage limited cement"])
    aggregate_type = st.sidebar.selectbox("Aggregate Type", options=["Limestone aggregate", "Local crashed limestone aggregate"])
    cement_kg_per_m3 = st.sidebar.number_input("Cement (kg/m³)", min_value=0.0, step=1.0)
    Fine__kg_per_m3 = st.sidebar.number_input("Fine Aggregate (kg/m³)", min_value=0.0, step=1.0)
    coarse_agg__kg_per_m3 = st.sidebar.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, step=1.0)
    wc_ratio_percent = st.sidebar.number_input("Water-Cement Ratio (%)", min_value=0.0, max_value=100.0, step=1.0)
    fly_ash_ggbfs_kg_per_m3 = st.sidebar.number_input("Fly Ash/GGBFS (kg/m³)", min_value=0.0, step=1.0)
    admixture_lit_per_m3 = st.sidebar.number_input("Admixture (liters/m³)", min_value=0.0, step=0.1)
    steel_fiber_aspect_ratio = st.sidebar.number_input("Steel Fiber Aspect Ratio", min_value=0.0, step=1.0)
    steel_fiber_percent = st.sidebar.number_input("Steel Fiber (%)", min_value=0.0, max_value=100.0, step=0.1)
    sample_surface_area_mm2 = st.sidebar.number_input("Sample Surface Area (mm²)", min_value=0.0, step=1.0)
    depth_mm = st.sidebar.number_input("Depth (mm)", min_value=0.0, step=1.0)
    relative_humidity_percent = st.sidebar.number_input("Relative Humidity (%)", min_value=0.0, max_value=100.0, step=1.0)
    temperature_c = st.sidebar.number_input("Temperature (°C)", min_value=-50.0, max_value=100.0, step=1.0)
    compressive_cylindrical_strength_mpa = st.sidebar.number_input("Compressive Cylindrical Strength (MPa)", min_value=0.0, step=1.0)
    curing_time_days = st.sidebar.number_input("Curing Time (days)", min_value=0.0, step=1.0)
    Loading__compressive_stress_mpa = st.sidebar.number_input("Loading Compressive Stress (MPa)", min_value=0.0, step=0.1)
    loading_time_days = st.sidebar.number_input("Loading Time (days)", min_value=0.0, step=1.0)

    # Create a DataFrame for input
    input_data = pd.DataFrame({
        'cement type': [cement_type],
        'Aggregate type': [aggregate_type],
        'cement (Kg/m³)': [cement_kg_per_m3],
        'Fine  (Kg/m³)': [Fine__kg_per_m3],
        'coarse agg  (Kg/m³)': [coarse_agg__kg_per_m3],
        'W/C ratio(%)': [wc_ratio_percent],
        'Fly Ash+ GGBFS(Kg/m³)': [fly_ash_ggbfs_kg_per_m3],
        ' admixture (Lit/m³)': [admixture_lit_per_m3],
        'SF aspect ratio': [steel_fiber_aspect_ratio],
        'steel fiber %': [steel_fiber_percent],
        'Sample Surface area (mm²)': [sample_surface_area_mm2],
        'depth(mm)': [depth_mm],
        'RH (%)': [relative_humidity_percent],
        'T (˚C)': [temperature_c],
        'fck': [compressive_cylindrical_strength_mpa],
        'curing time days': [curing_time_days],
        'Loading  Compressive stress(Mpa)': [Loading__compressive_stress_mpa],
        'loading time (days)': [loading_time_days]
    })

    return input_data

# Get user input
user_input = get_user_input()

# Display user input
st.subheader("User Input Parameters")
st.write(user_input)

# Make Prediction
if st.button("Predict"):
    try:
        # Transform the input data
        transformed_data = transformer.transform(user_input)

        # Make prediction
        prediction = model.predict(transformed_data)

        # Display prediction result
        st.success(f"Predicted Creep Strain Value: {prediction[0]:.4f} μm")

    except Exception as e:
        st.error(f"An error occurred: {e}")

