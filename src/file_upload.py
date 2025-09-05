from io import BytesIO
import pandas as pd
from docx import Document
import pdfplumber
from PIL import Image
import pytesseract
# import openpyxl
import pytesseract
def load_file_from_upload(uploaded):
    filename = uploaded.name
    ext = filename.split(".")[-1].lower()

    # Handle CSV
    if ext == "csv":
        df = pd.read_csv(uploaded)
        return "dataframe", df

    # Handle Excel
    elif ext == "xlsx":
        df = pd.read_excel(uploaded)
        return "dataframe", df

    # Handle TXT
    elif ext == "txt":
        text = uploaded.read().decode("utf-8")
        return "text", text

    # Handle DOCX
    elif ext == "docx":
        doc = Document(uploaded)
        text = "\n".join([para.text for para in doc.paragraphs])
        return "text", text

    # Handle PDF
    elif ext == "pdf":
        with pdfplumber.open(uploaded) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return "text", text

    # ✅ Handle Image (JPG/PNG)
    elif ext in ["jpg", "jpeg", "png"]:
        image = Image.open(uploaded)
        try:
            text = pytesseract.image_to_string(image)
            print(text)
            if not text.strip():
                return "text", "❌ OCR could not extract any meaningful text from the image."
            return "text", text
        except Exception as e:
            return "text", f"❌ OCR failed with error: {str(e)}"


    else:
        return "text", f"❌ Unsupported file type: {ext}"
