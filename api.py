from flask import Flask, request, render_template, send_file, redirect, url_for
import os, uuid
from converter import convert_input
from ai_module import call_llm
from anonimleştirici import process_table
from audit_trail import add_audit_trail
from data_validator import validate_all
from sablon_yonetici import apply_template
from save_to_excel import save_as_excel

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return redirect(url_for('index'))

    _, ext = os.path.splitext(uploaded_file.filename)
    unique_name = f"{uuid.uuid4()}{ext}"
    input_path = os.path.join(UPLOAD_FOLDER, unique_name)
    uploaded_file.save(input_path)

    print("🔄 Ham veri çıkarılıyor...")
    raw = convert_input(input_path)
    print("🤖 AI katmanına gönderiliyor...")
    parsed = call_llm(raw)
    print("🔒 Anonimleştirici çalışıyor...")
    parsed = process_table(parsed)
    print("🕵️ Audit trail ekleniyor...")
    parsed = add_audit_trail(parsed, source_file=input_path, file_type=ext[1:])
    print("✅ Veri validasyonu...")
    parsed = validate_all(parsed, interactive=False)
    # Şablon ismini formdan almak istersen: template = request.form.get("template")
    # parsed = apply_template(parsed, template)
    print("💾 Excel’e yazılıyor...")
    output_name = f"out_{uuid.uuid4()}.xlsx"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    save_as_excel(parsed, output_path)
    print("✅ Bitti.")

    return redirect(url_for('download', filename=output_name))

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        return redirect(url_for('index'))
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
