# anonimleştirici.py
import re

def mask_name(name):
    if not name or len(name) < 2:
        return "*"
    return name[0] + "*" * (len(name)-1)

def mask_tckn(tckn):
    if not tckn.isdigit() or len(tckn) != 11:
        return "*" * len(tckn)
    return tckn[:3] + "*"*6 + tckn[-2:]

def mask_email(email):
    try:
        user, domain = email.split("@")
        masked_user = user[0] + "***"
        domain_name, domain_ext = domain.split(".")
        masked_domain = domain_name[0] + "***"
        return f"{masked_user}@{masked_domain}.{domain_ext}"
    except Exception:
        return "*masked*"

def mask_phone(phone):
    digits = re.sub(r"\D", "", phone)
    if len(digits) != 11:
        return "*" * len(phone)
    return digits[:2] + "*"*6 + digits[-3:]

def is_name(key):
    return key.lower() in ("ad", "adı", "isim", "soyad", "soyadı", "name")

def is_tckn(val):
    return val.isdigit() and len(val) == 11

def is_email(val):
    return "@" in val and "." in val.split("@")[-1]

def is_phone(val):
    digits = re.sub(r"\D", "", val)
    return len(digits) == 11 and digits.startswith("05")

def detect_and_mask(row):
    value = str(row.get("Value", ""))
    key = str(row.get("Key", ""))
    anonim = value
    gizli = False

    if is_tckn(value):
        anonim = mask_tckn(value)
        gizli = True
    elif is_email(value):
        anonim = mask_email(value)
        gizli = True
    elif is_phone(value):
        anonim = mask_phone(value)
        gizli = True
    elif is_name(key):
        anonim = mask_name(value)
        gizli = True

    row_new = dict(row)
    row_new["Anonim"] = anonim
    row_new["Gizli"] = gizli
    return row_new

def process_table(rows):
    return [detect_and_mask(row) for row in rows]
