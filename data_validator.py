# data_validator.py

import re

def validate_row(row, row_idx):
    """
    Eksik veya hatalı alanları ve mantık/format hatalarını tespit eder.
    row: {"Key":..., "Value":..., "Type":...}
    """
    errors = []
    key = row.get("Key", "")
    value = row.get("Value", "")
    typ = row.get("Type", "")

    # 1. Boş Key, Value, Type kontrolü
    if not key:
        errors.append("Key boş")
    if not value:
        errors.append("Value boş")
    if not typ:
        errors.append("Type boş")

    # 2. Tip bazlı kontroller
    t = typ.lower()
    if t == "telefon":
        if not re.fullmatch(r"\d{10,13}", str(value)):
            errors.append("Telefon numarası hatalı (10-13 rakam olmalı)")
    if t == "tckn":
        if not re.fullmatch(r"\d{11}", str(value)):
            errors.append("TCKN 11 haneli olmalı")
    if t == "mail" or "mail" in key.lower():
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", str(value)):
            errors.append("E-posta formatı hatalı")
    if t == "tutar":
        if not re.fullmatch(r"\d+[.,]?\d*", str(value)):
            errors.append("Tutar sayısal değil")
    # ...ek mantıklar burada geliştirilebilir...

    return errors

def validate_all(data, interactive=False):
    """
    Tüm satırları kontrol eder, hataları loglar, opsiyonel interaktif düzeltme sunar.
    """
    error_log = []
    for i, row in enumerate(data):
        errors = validate_row(row, i)
        if errors:
            print(f"\n[Veri Kalite Hatası] Satır {i+1}: {errors}")
            error_log.append((i+1, errors.copy()))
            if interactive:
                cevap = input("Düzeltmek ister misin? (y/n): ").strip().lower()
                if cevap == "y":
                    for alan in ["Key", "Value", "Type"]:
                        if not row.get(alan):
                            yeni = input(f"{alan} alanını gir: ").strip()
                            row[alan] = yeni
    # Hata logunu kaydet
    if error_log:
        with open("error_log.txt", "a", encoding="utf-8") as f:
            for satir, errs in error_log:
                f.write(f"Satır {satir}: {', '.join(errs)}\n")
    return data
