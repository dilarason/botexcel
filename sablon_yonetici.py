# sablon_yonetici.py

# Basit şablonlar (kolon başlıklarını belirler)
TEMPLATES = {
    "fatura": ["Tarih", "Fatura No", "Müşteri", "Tutar", "Vergi", "Açıklama"],
    "personel": ["Adı", "Soyadı", "TC", "Departman", "Telefon", "E-posta"],
    "urun": ["Ürün Adı", "Barkod", "Fiyat", "Stok", "Kategori"],
    "klasik": ["Key", "Value", "Type", "Notes"],
}

def apply_template(data, template_name):
    """
    Sadece şablondaki alanları ve sıralamasını koruyarak yeni tablo döndürür.
    Eksik alan varsa "" ile doldurur.
    """
    template = TEMPLATES.get(template_name.lower())
    if not template:
        return data  # şablon yoksa olduğu gibi döndür

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
