import streamlit as st
import easyocr
import cv2
from tempfile import NamedTemporaryFile

# OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Glucose estimation
def estimate_glucose(fruit, brix):
    if fruit == "Watermelon":
        return round(brix * 10, 2)
    elif fruit == "Apple":
        return round(brix * 9.5 + 2, 2)
    elif fruit == "Guava":
        return round(brix * 8.8 + 1.5, 2)

# Extract Brix from image
def extract_brix(image_path):
    results = reader.readtext(image_path)
    for (_, text, _) in results:
        try:
            if "%" in text:
                text = text.replace("%", "")
            return float(text)
        except:
            continue
    return None

# Streamlit UI
st.title("🍉 Fruit Glucose Estimator")
fruit = st.selectbox("Select a fruit", ["Watermelon", "Apple", "Guava"])
uploaded_file = st.file_uploader("Upload a photo of the refractometer", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.image(tmp_path, caption="Uploaded Image", use_column_width=True)

    brix = extract_brix(tmp_path)
    if brix:
        glucose = estimate_glucose(fruit, brix)
        st.success(f"Brix: {brix}%")
        st.info(f"Estimated Glucose: {glucose} g/L")
    else:
        st.error("Could not detect a Brix value.")
