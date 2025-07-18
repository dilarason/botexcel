# barcode_module.py
# 🔹 Barkod okuma işlemlerini sağlayacak modül

from PIL import Image
from pyzbar.pyzbar import decode
import fitz
import mimetypes

def handle_barcode(file_path):
    """
    PDF veya resim dosyalarındaki barkodları algoritmik olarak tespit eder.
    Sadece PDF ve image/* tiplerinde çalışır.
    """
    barcodes = []
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type == "application/pdf":
        doc = fitz.open(file_path)
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            for obj in decode(img):
                barcodes.append(obj.data.decode("utf-8"))
        doc.close()

    elif mime_type and mime_type.startswith("image/"):
        img = Image.open(file_path)
        for obj in decode(img):
            barcodes.append(obj.data.decode("utf-8"))

    return barcodes
