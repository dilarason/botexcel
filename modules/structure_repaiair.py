#!/usr/bin/env python3
"""
converter.py

Girdi dosyasını (PDF, görüntü, TXT, CSV) tablo yapısına dönüştüren fonksiyonları içerir.
Ayrıca Structure Repair modülünü kullanarak bozuk hizalamaları otomatik olarak düzeltir.
"""
import os
import fitz  # PyMuPDF
import pytesseract
import cv2
import pandas as pd
from modules.structure_repair import repair_structure


def convert_input(file_path: str) -> list:
    """
    file_path: PDF, JPG, PNG, TXT veya CSV olabilir.
    - PDF: sayfa sayfa metni çekilir, satırlara bölünür.
    - Görsel: OCR ile metin çıkarılır.
    - TXT/CSV: doğrudan okunur.
    Çıktı: liste listeleri (her satır bir liste).
    """
    basename, ext = os.path.splitext(file_path)
    ext = ext.lower()
    raw_lines = []

    if ext == '.pdf':
        doc = fitz.open(file_path)
        for page in doc:
            text = page.get_text()
            raw_lines.extend(text.splitlines())
    elif ext in ['.jpg', '.jpeg', '.png']:
        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        raw_lines = text.splitlines()
    elif ext in ['.txt', '.csv']:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_lines = f.read().splitlines()
    else:
        raise ValueError(f"Desteklenmeyen dosya uzantısı: {ext}")

    # Ham satırları tabloya ayır (virgül veya sekme ile)
    data = []
    for line in raw_lines:
        if ',' in line:
            data.append([cell.strip() for cell in line.split(',')])
        elif '\t' in line:
            data.append([cell.strip() for cell in line.split('\t')])
        else:
            # Eğer tek sütun varsa bile liste halinde ekle
            data.append([line.strip()])

    # DataFrame oluştur ve yapıyı onar
    df = pd.DataFrame(data)
    df = repair_structure(df)

    # Final: temiz tablo verisini geri döndür
    return df.values.tolist()
