import streamlit as st
import easyocr
import cv2
import numpy as np
from PIL import Image
import re

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Streamlit app
st.title("Glucose Level Estimator")

# Add a dropdown menu for fruit selection
fruit = st.selectbox("Select a fruit:", ["Watermelon", "Apple", "Guava"])

# Capture image from webcam
st.write("Click the button below to capture an image from your webcam.")
uploaded_file = st.file_uploader("Upload an image captured from your refractometer", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file)
    frame_rgb = np.array(image)

    # Perform OCR
    results = reader.readtext(frame_rgb)

    # Debug: Show OCR results
    st.write("OCR Results:", results)

    # Extract Brix value
    brix_value = None
    for (bbox, text, prob) in results:
        try:
            # Clean the text to remove unwanted characters
            cleaned_text = re.sub(r"[^0-9\.,%]", "", text)

            if "%" in cleaned_text:
                cleaned_text = cleaned_text.replace(",", ".")  # Replace comma with dot if needed
                cleaned_text = cleaned_text.replace("%", "")   # Remove percent symbol
                brix_value = float(cleaned_text)
                break
        except ValueError:
            continue

    if brix_value is not None:
        # Estimate glucose levels for different fruits
        def estimate_glucose(fruit, brix):
            if fruit == "Watermelon":
                return round(brix * 10, 2)
            elif fruit == "Apple":
                return round(brix * 9.5 + 2, 2)
            elif fruit == "Guava":
                return round(brix * 8.8 + 1.5, 2)
            else:
                return None

        # Estimate glucose levels for the selected fruit
        glucose = None
        if fruit:
            glucose = estimate_glucose(fruit, brix_value)

        # Display Brix and Glucose values in a nicer format
        st.markdown(f"### Brix Value: **{brix_value}%**")
        if glucose is not None:
            st.markdown(f"### Estimated Glucose for **{fruit}**: **{glucose} g/L**")
        else:
            st.markdown("### Could not estimate glucose for the selected fruit.")
    else:
        st.markdown("### Could not extract Brix value from the image.")
