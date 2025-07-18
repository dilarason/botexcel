# test_data.py

from data_validator import validate_all

test_data = [
    {"Key": "Telefon", "Value": "0532123abc", "Type": "Telefon"},
    {"Key": "TCKN", "Value": "1234567890", "Type": "TCKN"},
    {"Key": "E-Posta", "Value": "ali#mail.com", "Type": "Mail"},
    {"Key": "Tutar", "Value": "12x5,67", "Type": "Tutar"},
    {"Key": "", "Value": "123", "Type": "Tutar"},
]

if __name__ == "__main__":
    validate_all(test_data, interactive=True)
