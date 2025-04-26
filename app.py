import re

# Perform OCR
results = reader.readtext(frame_rgb)

# Extract Brix value
brix_value = None
for (bbox, text, prob) in results:
    try:
        # Remove any non-number, non-dot, non-comma, non-percent characters
        cleaned_text = re.sub(r"[^0-9\.,%]", "", text)

        if "%" in cleaned_text:
            cleaned_text = cleaned_text.replace(",", ".")  # In case comma used instead of dot
            cleaned_text = cleaned_text.replace("%", "")   # Remove percent symbol
            brix_value = float(cleaned_text)
            break
    except ValueError:
        continue
