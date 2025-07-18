# save_to_excel.py
from openpyxl import Workbook
from kumeleyici_rapor import group_and_summary, add_summary_sheet

def save_as_excel(data, output_path="output.xlsx"):
    """
    Hem asıl tabloyu, hem de gruplama sheet’ini kaydeder.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Veri"

    # Başlık satırı
    if data and isinstance(data[0], dict):
        ws.append(list(data[0].keys()))
    else:
        return  # boş veri

    for row in data:
        ws.append([row.get(k, "") for k in data[0].keys()])

    # Özet tablosu ekle
    summary_data = group_and_summary(data, group_key="Key")  # Burada istersen başka alan kullanabilirsin
    add_summary_sheet(wb, summary_data, sheet_name="Summary")

    wb.save(output_path)
    print(f"💾 Kaydedildi: {output_path}")
