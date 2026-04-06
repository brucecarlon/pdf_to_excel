import os
import cv2
import pytesseract
import pandas as pd
from pdf2image import convert_from_path

# ----------------------------
# Paths
# ----------------------------
PDF_PATH = "./Deeds office january 2026.pdf"
IMAGE_DIR = "images"
OUTPUT_FILE = "output/deeds_office_jan_2026.xlsx"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)

# ----------------------------
# 1. Convert PDF → Images
# ----------------------------
print("Converting PDF to images...")

pages = convert_from_path(PDF_PATH, dpi=300)

image_files = []
for i, page in enumerate(pages):
    img_path = f"{IMAGE_DIR}/page_{i}.png"
    page.save(img_path, "PNG")
    image_files.append(img_path)

print(f"Saved {len(image_files)} images.")

# ----------------------------
# 2. Image cleanup for OCR
# ----------------------------
def preprocess_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Increase contrast + binarize
    img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)[1]

    return img

# ----------------------------
# 3. OCR images
# ----------------------------
print("Running OCR...")

all_lines = []

for img_path in image_files:
    cleaned = preprocess_image(img_path)

    text = pytesseract.image_to_string(
        cleaned,
        config="--psm 6"
    )

    lines = [line for line in text.split("\n") if line.strip()]
    all_lines.extend(lines)
    print("---- OCR SAMPLE ----")
    print(text[:300])

print(f"OCR extracted {len(all_lines)} lines.")

# ----------------------------
# 4. Parse lines into columns
# ----------------------------
rows = []

for line in all_lines:
    if line.strip():
        rows.append([line])  # keep full line as one column

print(f"Total lines captured: {len(rows)}")

df = pd.DataFrame(rows, columns=["Raw Text"])

df = pd.DataFrame(rows)

# ----------------------------
# 5. Export to Excel
# ----------------------------
df.to_excel(OUTPUT_FILE, index=False, header=False)

print(f"Excel file written to: {OUTPUT_FILE}")