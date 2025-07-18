# main.py
# 🔹 CLI: convert_input → call_llm → save_as_excel
# Hata yönetimi ve logging ekli

import sys                    # Komut satırı argümanları için
import os                     # Dosya işlemleri için
import logging                # Loglama için

from converter import convert_input
from ai_module import call_llm
from save_to_excel import save_as_excel

# Log klasörü oluştur
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    try:
        if len(sys.argv) < 2:
            msg = "Kullanım: python main.py <giriş_dosyası> [<çıkış_dosyası>]"
            print(msg)
            logging.error("Eksik argüman ile çalıştırıldı.")
            sys.exit(1)

        inp = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else "output.xlsx"

        if not os.path.exists(inp):
            print("Dosya bulunamadı:", inp)
            logging.error(f"Girdi dosyası bulunamadı: {inp}")
            sys.exit(1)

        print("🔄 Ham veri çıkarılıyor...")
        logging.info(f"Girdi dosyası işleniyor: {inp}")
        try:
            raw = convert_input(inp)
        except Exception as e:
            print("Ham veri çıkarılırken hata oluştu.")
            logging.error(f"convert_input hata: {e}", exc_info=True)
            sys.exit(1)

        print("🤖 AI katmanına gönderiliyor...")
        try:
            parsed = call_llm(raw)
        except Exception as e:
            print("AI işleminde hata oluştu.")
            logging.error(f"call_llm hata: {e}", exc_info=True)
            sys.exit(1)

        print("💾 Excel’e yazılıyor...")
        try:
            save_as_excel(parsed, out)
        except Exception as e:
            print("Excel'e kaydedilirken hata oluştu.")
            logging.error(f"save_as_excel hata: {e}", exc_info=True)
            sys.exit(1)

        print("✅ Tamamlandı:", out)
        logging.info(f"CLI işlem başarıyla tamamlandı. Çıktı: {out}")

    except Exception as e:
        # Herhangi beklenmeyen büyük hata için
        print("Beklenmeyen bir hata oluştu. Detaylar logda.")
        logging.error(f"main.py genel hata: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
