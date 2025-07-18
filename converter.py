# converter.py

import mimetypes
import fitz
from PIL import Image
import pytesseract
from barcode_module import handle_barcode

def convert_input(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    data = []

    if mime_type == "application/pdf":
        barcodes = handle_barcode(file_path)
        data.extend(f"BARCODE: {c}" for c in barcodes)
        doc = fitz.open(file_path)
        for page in doc:
            text = page.get_text().strip()
            if text:
                data.append(text)
        doc.close()

    elif mime_type == "text/plain":
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append(line)

    elif mime_type and mime_type.startswith("image/"):
        barcodes = handle_barcode(file_path)
        data.extend(f"BARCODE: {c}" for c in barcodes)
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang="tur")
        for line in text.splitlines():
            line = line.strip()
            if line:
                data.append(line)

    else:
        # desteklenmeyen
        pass

    return data
