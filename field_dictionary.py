import json
import os

# Sözlük dosyası yolu
DICT_PATH = "field_dict.json"

def load_field_dict():
    """Alan sözlüğünü dosyadan yükler, yoksa boş başlatır."""
    if os.path.exists(DICT_PATH):
        with open(DICT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_field_dict(field_dict):
    """Alan sözlüğünü dosyaya kaydeder."""
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(field_dict, f, ensure_ascii=False, indent=2)

def ask_field_type(key, interactive=False):
    if not interactive:
        return {"Type": "Unknown", "Desc": ""}
    print(f"\n[Alan Sözlüğü] Yeni başlık tespit edildi: '{key}'")
    type_ = input("Bu alanın tipi nedir? (ör: Kişi, Barkod, Tutar, Tarih, Ürün): ").strip()
    desc = input("Açıklama (isteğe bağlı): ").strip()
    return {"Type": type_, "Desc": desc}

def update_field_dict_for_keys(keys, field_dict, interactive=False):
    changed = False
    for key in keys:
        if key not in field_dict:
            info = ask_field_type(key, interactive=interactive)
            field_dict[key] = info
            changed = True
    if changed:
        save_field_dict(field_dict)
    return field_dict

