from audit_trail import add_audit_trail

data = [
    {"Key": "Adı", "Value": "Ahmet", "Type": "Kişi"},
    {"Key": "BARCODE", "Value": "12345", "Type": "Barkod"}
]
# Varsayalım bu veri "fatura1.pdf" dosyasından geldi:
data = add_audit_trail(data, source_file="fatura1.pdf", file_type="pdf")
print(data)
