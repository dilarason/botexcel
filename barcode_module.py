# barcode_module.py
# 🔹 Barkod okuma işlemlerini sağlayacak modül (hata yönetimi ve loglama ekli)

from PIL import Image                    # Görsel işleme için
from pyzbar.pyzbar import decode         # Barkod okuma için
import fitz                              # PDF işlemleri için
import mimetypes                         # Dosya türü kontrolü için
import logging                           # Loglama için
import os                                # Klasör yönetimi için

# Log klasörü ve ayarları
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def handle_barcode(file_path):
    """
    PDF veya resim dosyalarındaki barkodları algoritmik olarak tespit eder.
    Sadece PDF ve image/* tiplerinde çalışır.
    Hata oluşursa loglar.
    """
    barcodes = []
    try:
        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type == "application/pdf":
            try:
                doc = fitz.open(file_path)
                for page in doc:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    for obj in decode(img):
                        barcodes.append(obj.data.decode("utf-8"))
                doc.close()
                logging.info(f"{file_path} PDF'den barkodlar başarıyla okundu.")
            except Exception as e:
                logging.error(f"{file_path} PDF'den barkod okuma hatası: {e}", exc_info=True)

        elif mime_type and mime_type.startswith("image/"):
            try:
                img = Image.open(file_path)
                for obj in decode(img):
                    barcodes.append(obj.data.decode("utf-8"))
                logging.info(f"{file_path} görselden barkodlar başarıyla okundu.")
            except Exception as e:
                logging.error(f"{file_path} görselden barkod okuma hatası: {e}", exc_info=True)

        else:
            logging.warning(f"{file_path} barkod için desteklenmeyen dosya tipi: {mime_type}")

    except Exception as e:
        logging.error(f"handle_barcode genel hata: {e}", exc_info=True)

    return barcodes
