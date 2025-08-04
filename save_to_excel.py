# save_to_excel.py
from openpyxl import Workbook
import logging, os
from datetime import datetime

from sablon_yonetici import apply_template
from audit_trail import add_audit_trail
from data_validator import validate_all, validate_row  # validate_row eklendi!
from field_dictionary import load_field_dict, update_field_dict_for_keys
from kumeleyici_rapor import group_and_summary, add_summary_sheet

# ... (log ayarları aynı)

def add_metadata_sheet(wb, meta: dict, sheet_name="Metadata"):
    ws = wb.create_sheet(title=sheet_name)
    for k, v in meta.items():
        ws.append([k, v])

def save_as_excel(
    data,
    output_path="output.xlsx",
    *,
    template="klasik",
    input_file=None,
    file_type="txt",
    interactive=False
):
    try:
        data = apply_template(data, template)
        field_dict = load_field_dict()
        all_keys = [row.get("Key", "") for row in data if row.get("Key")]
        field_dict = update_field_dict_for_keys(all_keys, field_dict)
        for row in data:
            key = row.get("Key", "")
            if key and not row.get("Type") and key in field_dict:
                row["Type"] = field_dict[key].get("Type", "")

        # ---- 🔴 DOĞRULAMA HATALARINI TOPLA ----
        errors = []
        for i, row in enumerate(data):
            row_errors = validate_row(row, i)
            if row_errors:
                for err in row_errors:
                    errors.append(f"Satır {i+1}: {err}")

        if errors:
            # Hataları istisna olarak döndür
            error_text = "Veri doğrulama hatası!<br>" + "<br>".join(errors)
            raise RuntimeError(error_text)
        # ---------------------------------------

        data = validate_all(data, interactive=interactive)
        if input_file:
            data = add_audit_trail(data, input_file, file_type=file_type)

        wb = Workbook()
        ws = wb.active
        ws.title = "Veri"
        headers = list(data[0].keys()) if data else ["Key", "Value", "Type", "Notes"]
        ws.append(headers)
        for row in data:
            ws.append([row.get(k, "") for k in headers])

        summary = group_and_summary(data, group_key="Key")
        add_summary_sheet(wb, summary, sheet_name="Özet")

        meta = {
            "Uygulama": "BotExcel.Ai",
            "İşlem Yapan": "Anonim",
            "Kaynak Dosya": os.path.basename(input_file) if input_file else "",
            "Dönüştürme Zamanı": datetime.now().isoformat(timespec="seconds"),
            "Şablon": template,
            "Dosya Tipi": file_type,
        }
        add_metadata_sheet(wb, meta)
        wb.save(output_path)
        logging.info(f"Excel başarıyla kaydedildi: {output_path}")

    except Exception as e:
        logging.error(f"Excel kaydedilirken hata: {e}", exc_info=True)
        raise RuntimeError(str(e))
