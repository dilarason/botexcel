# test_main.py

from test_data import test_data
from anonimleştirici import process_table
from audit_trail import add_audit_trail
from data_validator import validate_all
from sablon_yonetici import apply_template
from kumeleyici_rapor import group_and_summary

# 1. Kişisel veri maskele
data = process_table(test_data)

# 2. Audit trail ekle
data = add_audit_trail(data, source_file="test.txt", file_type="txt")

# 3. Veri kalite/hata kontrolü
data = validate_all(data)

# 4. Şablon uygula (örnek: klasik)
data = apply_template(data, "klasik")  # "fatura", "personel" vb. seçebilirsin

# 5. Gruplama ve özet
summary = group_and_summary(data, group_key="Key")
print("Summary (Key bazlı sayım):")
for row in summary:
    print(row)

# 6. İstersen save_to_excel ile kaydedebilirsin
# from save_to_excel import save_as_excel
# save_as_excel(data, "test_output.xlsx")
