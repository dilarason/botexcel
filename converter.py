# converter.py

import os
import mimetypes
import fitz  # PDF için
from PIL import Image
import pytesseract

def convert_input(file_path):
    """
    Giriş dosyasının türüne göre uygun işleme yönlendirir.
    """
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type == "application/pdf":
        print("📄 PDF dosyası algılandı.")
        return handle_pdf(file_path)

    elif mime_type == "text/plain":
        print("📄 Metin dosyası algılandı.")
        return handle_text(file_path)

    elif mime_type and mime_type.startswith("image/"):
        print("🖼️ Görsel dosyası algılandı.")
        return handle_image(file_path)

    else:
        print("❌ Desteklenmeyen dosya türü:", mime_type)
        return []

# PDF okuma
def handle_pdf(path):
    try:
        doc = fitz.open(path)
        text_list = [page.get_text() for page in doc]
        doc.close()
        return text_list
    except Exception as e:
        print("❌ PDF işleme hatası:", e)
        return []

# TXT okuma
def handle_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except Exception as e:
        print("❌ Metin işleme hatası:", e)
        return []

# Görsel OCR
def handle_image(path):
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img, lang="tur")
        return text.splitlines()
    except Exception as e:
        print("❌ Görsel işleme hatası:", e)
        return []
