# save_to_excel.py

# 🔹 Gerekli kütüphaneyi içe aktar
import openpyxl  # Excel dosyası oluşturmak için

# 🔹 Excel dosyasına veri kaydeden fonksiyon
def save_as_excel(data, output_path="output.xlsx"):
    """
    Yapılandırılmış liste verisini bir Excel dosyasına yazar.
    Varsayılan çıktı dosyası adı: output.xlsx
    """

    # Yeni bir Excel çalışma kitabı oluştur
    workbook = openpyxl.Workbook()

    # İlk sayfayı seç
    sheet = workbook.active

    # Her satırı sırayla yaz
    for i, row in enumerate(data, start=1):
        sheet.cell(row=i, column=1, value=row)

    # Dosyayı kaydet
    workbook.save(output_path)

    print(f"💾 Excel dosyası kaydedildi: {output_path}")
