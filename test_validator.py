from data_validator import validate_all

data = [
    {"Key": "", "Value": "12345", "Type": "Barkod"},
    {"Key": "Fiyat", "Value": "", "Type": "Tutar"},
    {"Key": "Tarih", "Value": "2024-10-05", "Type": ""},
    {"Key": "Telefon", "Value": "abc123", "Type": "Telefon"}
]

data = validate_all(data)
print(data)
