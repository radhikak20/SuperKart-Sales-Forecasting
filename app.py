import streamlit as st
import pandas as pd
import requests
import json

# --- Streamlit UI Setup ---
st.set_page_config(page_title="SuperKart Sales Predictor", layout="centered")
st.title("🛒 SuperKart Sales Predictor")
st.write("Enter product and store details to forecast sales revenue.")

# Backend API endpoint (placeholder for now)
# Replace with your deployed backend URL
BACKEND_URL = "https://NextGenModelCraft-SuperKartBackend.hf.space/v1/predict"

# --- Input Fields ---
st.header("Product Details")
product_weight = st.number_input("Product Weight (kg)", min_value=0.1, max_value=50.0, value=12.0, step=0.1)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ("Low Sugar", "Regular", "No Sugar")
)

product_allocated_area = st.number_input("Product Allocated Area Ratio", min_value=0.001, max_value=0.5, value=0.05, format="%.3f", step=0.001)

product_mrp = st.number_input("Product MRP (Maximum Retail Price)", min_value=1.0, max_value=500.0, value=150.0, step=0.1)

product_id_char = st.selectbox(
    "Product ID Category (First two chars of Product_Id)",
    ("FD", "NC", "DR")
)

product_type_category = st.selectbox(
    "Product Type Category",
    ("Non Perishables", "Perishables")
)

st.header("Store Details")
store_size = st.selectbox(
    "Store Size",
    ("Medium", "High", "Small")
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ("Tier 1", "Tier 2", "Tier 3")
)

store_type = st.selectbox(
    "Store Type",
    ("Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart")
)

store_age_years = st.number_input("Store Age (Years)", min_value=1, max_value=100, value=20, step=1)

# --- Prediction Button ---
if st.button("Forecast Sales"):
    # Prepare input data as a dictionary
    input_data = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age_years,
        "Product_Type_Category": product_type_category,
    }

    # Convert to JSON string
    json_data = json.dumps(input_data)

    st.write(f"Sending request to: {BACKEND_URL}")
    st.json(input_data)

    try:
      response = requests.post("https://NextGenModelCraft-SuperKartBackend.hf.space/v1/predict", json=input_data)
    # Check if response is successful
      if response.status_code == 200:
          # Check if response has content before parsing
          if response.text.strip():
              try:
                  prediction = response.json().get("prediction")
                  if prediction is not None:
                      st.success(f"Predicted Sales Revenue: ₹{prediction:,.2f}")
                  else:
                      st.error("Backend returned empty prediction")
              except requests.exceptions.JSONDecodeError:
                  st.error(f"Backend returned invalid JSON: {response.text[:200]}")
          else:
              st.error("Backend returned empty response")
      else:
          st.error(f"Error from backend: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Please ensure the backend is running and the URL is correct.")
    except requests.exceptions.Timeout:
        st.error("Request timed out. The backend is taking too long to respond.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
