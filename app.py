import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

st.title("🍉🍎 Guava Glucose Estimator")

# 1. Select a fruit
fruit = st.selectbox("Select a fruit:", ["Watermelon", "Apple", "Guava"])

# 2. Upload an image
uploaded_file = st.file_uploader("Upload an image of the refractometer reading", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to numpy array for OCR
    img_np = np.array(image)

    # 3. Run OCR on image
    with st.spinner("Extracting Brix value..."):
        results = reader.readtext(img_np)

    # 4. Extract Brix value from OCR results
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
        # 5. Estimate glucose based on selected fruit
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

        # 6. Display results
        st.markdown(f"### 🧪 Brix Value: **{brix_value}%**")
        st.markdown(f"### 🍬 Estimated Glucose for **{fruit}**: **{glucose} g/L**")
    else:
        st.error("❌ Could not extract a valid Brix value from the image.")
