import streamlit as st
import easyocr
import cv2
import numpy as np
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Streamlit app
st.title("Glucose Level Estimator")

# Add a dropdown menu for fruit selection
fruit = st.selectbox("Select a fruit:", ["Watermelon", "Apple", "Guava"])

# Capture image from webcam
st.write("Click the button below to capture an image from your webcam.")
start_capture = st.button("Capture Image")

if start_capture:
    # Access the webcam
    cap = cv2.VideoCapture(0)  # Use 1 for the second webcam
    ret, frame = cap.read()
    cap.release()

    if ret:
        # Convert the captured frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform OCR
        results = reader.readtext(frame_rgb)

        # Extract Brix value and calculate glucose
        brix_value = None
        for (bbox, text, prob) in results:
            try:
                if "%" in text:
                    text = text.replace("%", "")
                brix_value = float(text)
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

            # Display Brix and Glucose values in a more appealing format
            st.markdown(f"### Brix Value: **{brix_value}%**")
            if glucose is not None:
                st.markdown(f"### Estimated Glucose for **{fruit}**: **{glucose} g/L**")
            else:
                st.markdown("### Could not estimate glucose for the selected fruit.")
        else:
            st.markdown("### Could not extract Brix value from the image.")
    else:
        st.markdown("### Failed to capture image from webcam.")
