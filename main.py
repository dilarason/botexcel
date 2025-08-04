# main.py
# 🔹 CLI: AI → Şablon → Doğrulama → Audit → Excel yazım zinciri

import sys, os, logging
from converter import convert_input
from ai_module import call_llm
from save_to_excel import save_as_excel

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
            print("Kullanım: python main.py <girdi_dosyası> [<çıkış_dosyası>] [<şablon_adı>]")
            sys.exit(1)

        inp = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else "output.xlsx"
        template = sys.argv[3] if len(sys.argv) > 3 else "klasik"

        if not os.path.exists(inp):
            print("❌ Dosya bulunamadı:", inp)
            sys.exit(1)

        print("🔄 Ham veri çıkarılıyor...")
        raw = convert_input(inp)

        print("🤖 AI modeline gönderiliyor...")
        parsed = call_llm(raw)

        print(f"📊 '{template}' şablonuyla Excel'e yazılıyor...")
        ext = os.path.splitext(inp)[1].lstrip('.').lower()
        save_as_excel(parsed, out, template=template, input_file=inp, file_type=ext, interactive=False)

        print("✅ İşlem tamamlandı:", out)

    except Exception as e:
        print("💥 Hata oluştu:", e)

if __name__ == "__main__":
    main()
