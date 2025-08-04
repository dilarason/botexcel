# sablon_yonetici.py

# Basit şablonlar (kolon başlıklarını belirler)
TEMPLATES = {
    "fatura": ["Tarih", "Fatura No", "Müşteri", "Tutar", "Vergi", "Açıklama"],
    "personel": ["Adı", "Soyadı", "TC", "Departman", "Telefon", "E-posta"],
    "urun": ["Ürün Adı", "Barkod", "Fiyat", "Stok", "Kategori"],
    "klasik": ["Key", "Value", "Type", "Notes"],
}

def apply_template(data, template_name):
    template = TEMPLATES.get(template_name.lower(), [])
    new_data = []
    for row in data:
        new_row = {col: "" for col in template}
        for col in template:
            for key, value in row.items():
                if key.lower() == col.lower():
                    new_row[col] = value
        new_data.append(new_row)
    return new_data

    # Her satırı şablona göre diz
    new_data = []
    for row in data:
        new_row = {}
        for col in template:
            # AI çıkışındaki Key eşleşirse al, yoksa boş bırak
            if row.get("Key", "").lower() == col.lower():
                new_row[col] = row.get("Value", "")
            else:
                new_row[col] = ""
        new_data.append(new_row)
    return new_data
