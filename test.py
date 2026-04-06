from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import cv2
import pandas as pd
import numpy as np

# 1️⃣ Test pdf2image
try:
    # Create a blank PDF page as test
    from io import BytesIO
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    pdf_file = "test.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.drawString(100, 750, "Hello, PDF2Image Test!")
    c.save()

    images = convert_from_path(pdf_file)
    print("PDF to Image conversion: ✅ Success")
except Exception as e:
    print("PDF to Image conversion: ❌ Failed", e)

# 2️⃣ Test pytesseract
try:
    # Convert first PDF page to image and OCR it
    text = pytesseract.image_to_string(images[0])
    print("OCR with pytesseract: ✅ Success")
    print("Extracted text:", text.strip())
except Exception as e:
    print("OCR with pytesseract: ❌ Failed", e)

# 3️⃣ Test OpenCV
try:
    img_array = np.array(images[0])
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    print("OpenCV image processing: ✅ Success")
except Exception as e:
    print("OpenCV image processing: ❌ Failed", e)

# 4️⃣ Test pandas & openpyxl
try:
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})
    df.to_excel("test.xlsx", index=False)
    df2 = pd.read_excel("test.xlsx")
    print("Pandas + OpenPyXL: ✅ Success")
    print(df2)
except Exception as e:
    print("Pandas + OpenPyXL: ❌ Failed", e)
