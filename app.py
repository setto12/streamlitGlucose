import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Streamlit app
st.title("Glucose Level Estimator")

# Dropdown menu for fruit selection
fruit = st.selectbox("Select a fruit:", ["Watermelon", "Apple", "Guava"])

# Upload image
uploaded_file = st.file_uploader("Upload a refractometer image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read uploaded image
    image = Image.open(uploaded_file)
    image_rgb = np.array(image)

    # Perform OCR
    results = reader.readtext(image_rgb)

    # Extract Brix value
    brix_value = None
    for (bbox, text, prob) in results:
        try:
            matches = re.findall(r"\d+\.\d+", text)
            if matches:
                brix_value = float(matches[0])
                break
        except ValueError:
            continue

    if brix_value is not None:
        # Estimate glucose levels in g/100mL
        def estimate_glucose(fruit, brix):
            if fruit == "Watermelon":
                return round(brix * 0.9, 2)
            elif fruit == "Apple":
                return round(brix * 0.95 + 0.2, 2)
            elif fruit == "Guava":
                return round(brix * 0.88 + 0.15, 2)
            else:
                return None

        glucose = estimate_glucose(fruit, brix_value)

        # Display result in g/100mL
        st.markdown(f"### Estimated Glucose for **{fruit}**: **{glucose} g/100mL**")
    else:
        st.markdown("### Could not extract Brix value from the image.")
