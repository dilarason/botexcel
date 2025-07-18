# main.py
import sys
import os
from converter import convert_input
from ai_module import call_llm
from anonimleştirici import process_table
from audit_trail import add_audit_trail
from data_validator import validate_all
from sablon_yonetici import apply_template
from save_to_excel import save_as_excel

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python main.py <giriş_dosyası> [<şablon_adı>] [<çıkış_dosyası>]")
        sys.exit(1)

    inp = sys.argv[1]
    template_name = sys.argv[2] if len(sys.argv) > 2 else None
    out = sys.argv[3] if len(sys.argv) > 3 else "output.xlsx"

    if not os.path.exists(inp):
        print("Dosya bulunamadı:", inp)
        sys.exit(1)

    print("🔄 Ham veri çıkarılıyor...")
    raw = convert_input(inp)

    print("🤖 AI katmanına gönderiliyor...")
    parsed = call_llm(raw)

    print("🔒 Kişisel veriler anonimleştiriliyor...")
    parsed_anon = process_table(parsed)

    print("🕵️ Audit trail ekleniyor...")
    file_ext = os.path.splitext(inp)[-1][1:]  # pdf, txt, vs.
    parsed_audit = add_audit_trail(parsed_anon, source_file=inp, file_type=file_ext)

    print("✅ Veri kalitesi/hata kontrolü yapılıyor...")
    validated_data = validate_all(parsed_audit, interactive=True)

    # Şablon opsiyonel
    if template_name:
        print(f"🗂 Şablon ({template_name}) uygulanıyor...")
        parsed_final = apply_template(validated_data, template_name)
    else:
        parsed_final = validated_data

    # Burada otomatik özet/pivot (kumeleyici_rapor) istersen, ekleyebilirsin
    # (Ekstra bir Excel sheet veya özet rapor için.)
    # from kumeleyici_rapor import group_and_summary, add_summary_sheet
    # summary_data = group_and_summary(parsed_final)
    # wb = save_as_excel(parsed_final, out, return_wb=True)
    # add_summary_sheet(wb, summary_data)
    # wb.save(out)

    print("💾 Excel’e yazılıyor...")
    save_as_excel(parsed_final, out)
    print("✅ Tamamlandı:", out)

if __name__ == "__main__":
    main()
