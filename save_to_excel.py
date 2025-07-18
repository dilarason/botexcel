# save_to_excel.py
# 🔹 AI’dan gelen dict listesini Excel’e dönüştürme (logging ve hata yönetimi ekli)

from openpyxl import Workbook          # Excel dosyası oluşturmak için
import logging                         # Loglama için
import os                              # Klasör ve dosya yönetimi için

# Log klasörü varsa yoksa oluştur
os.makedirs('logs', exist_ok=True)

# Loglama ayarları
logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def save_as_excel(data, output_path="output.xlsx"):
    """
    data: [
      {"Key":..., "Value":..., "Type":..., "Notes":...}, ...
    ]
    formatındaki listeyi Excel’e yazar.
    Hataları loglar.
    """
    try:
        wb = Workbook()               # Yeni Excel dosyası oluşturur
        ws = wb.active                # Aktif sayfayı seçer

        # Başlık satırı ekle
        ws.append(["Key", "Value", "Type", "Notes"])

        for row in data:
            # Her dict satırını ekle, eksik alanları boş bırak
            ws.append([
                row.get("Key", ""),
                row.get("Value", ""),
                row.get("Type", ""),
                row.get("Notes", "")
            ])

        wb.save(output_path)          # Excel dosyasını kaydet
        logging.info(f"Excel başarıyla kaydedildi: {output_path}")

    except Exception as e:
        # Hata oluşursa logla ve istisna fırlat
        logging.error(f"Excel kaydedilirken hata: {e}", exc_info=True)
        raise RuntimeError("Excel kaydedilemedi, detaylar logda.")

