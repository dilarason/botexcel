# audit_trail.py
# Her satıra audit-trail bilgisi ekler

from datetime import datetime
import os

def add_audit_trail(data, source_file, file_type="txt"):
    """
    Her satıra kaynak dosya adı, satır no, işlenme zamanı ve dosya tipini ekler.
    data: [{"Key":..., "Value":..., ...}, ...]
    source_file: "fatura1.pdf" gibi
    file_type: "pdf", "txt", "img" vb.
    """
    process_time = datetime.now().isoformat(timespec="seconds")
    for idx, row in enumerate(data):
        row["source_file"] = os.path.basename(source_file)
        row["source_row"] = idx + 1
        row["process_time"] = process_time
        row["file_type"] = file_type
    return data
