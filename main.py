# main.py

# 🔹 Gerekli modülleri içe aktar
import sys      # Komut satırı argümanlarını okuyabilmek için
import os       # Dosya kontrolü için

# 🔹 Diğer modülleri içe aktar
from converter import convert_input         # Veriyi dönüştürme fonksiyonu
from save_to_excel import save_as_excel     # Excel'e kaydetme fonksiyonu

# 🔹 Ana kontrol fonksiyonu
def main():
    # Komut satırında giriş dosyası verilmiş mi?
    if len(sys.argv) < 2:
        print("❌ Lütfen bir giriş dosyası belirtin.")
        sys.exit(1)

    # Giriş dosyasının yolunu al
    input_path = sys.argv[1]

    # Dosya mevcut mu?
    if not os.path.exists(input_path):
        print("❌ Dosya bulunamadı:", input_path)
        sys.exit(1)

    # Veriyi dönüştür
    structured_data = convert_input(input_path)

    # Excel'e yaz
    save_as_excel(structured_data)

    print("✅ Excel dosyası başarıyla oluşturuldu.")

# 🔹 Dosya doğrudan çalıştırılırsa, main() fonksiyonunu başlat
if __name__ == "__main__":
    main()
