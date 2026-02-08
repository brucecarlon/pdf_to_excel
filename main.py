from pdf2image import convert_from_path

pages = convert_from_path(
    "Deeds office january 2026.pdf",
    dpi=300,
    poppler_path=r"C:\poppler\Library\bin"
)

for i, page in enumerate(pages):
    page.save(f"page_{i}.png", "PNG")

import cv2

img = cv2.imread("page_0.png", 0)
img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("clean.png", img)

import pytesseract

text = pytesseract.image_to_string(
    "clean.png",
    config="--psm 6"
)

print(text)


import pandas as pd
rows = [r.split() for r in text.split("\n") if r.strip()]
df = pd.DataFrame(rows)
df.to_excel("output.xlsx", index=False)

convert_from_path(pdf, dpi=300)
