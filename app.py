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
start_capture = st.button("Capture Image")

if start_capture:
    # Access the webcam
    cap = cv2.VideoCapture(0)  # 0 is the default webcam
    ret, frame = cap.read()
    cap.release()

    if ret:
        # Convert the captured frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display captured image
        st.image(frame_rgb, caption="Captured Image", use_column_width=True)

        # Perform OCR
        results = reader.readtext(frame_rgb)

        # Debug: Show OCR raw results
        st.write("OCR Results:", results)

        # Extract Brix value
        brix_value = None
        for (bbox, text, prob) in results:
            try:
                # Find decimal numbers like 6.2, 10.5, etc.
                matches = re.findall(r"\d+\.\d+", text)
                if matches:
                    brix_value = float(matches[0])
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

            glucose = estimate_glucose(fruit, brix_value)

            # Display Brix and Glucose values
            st.markdown(f"### Brix Value: **{brix_value}%**")
            if glucose is not None:
                st.markdown(f"### Estimated Glucose for **{fruit}**: **{glucose} g/L**")
            else:
                st.markdown("### Could not estimate glucose for the selected fruit.")
        else:
            st.markdown("### Could not extract Brix value from the image.")
    else:
        st.markdown("### Failed to capture image from webcam.")
