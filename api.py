# api.py
# 🔹 REST API: Dosya yükle → AI ile ayrıştır → Excel’e dönüştür → İndir

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import logging
import magic  # Dosya türü (magic number) için
from flask_limiter import Limiter  # API rate limit için
from flask_limiter.util import get_remote_address

from converter import convert_input
from ai_module import call_llm
from save_to_excel import save_as_excel

# Log klasörü ve loglama ayarları
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# API için dosya uzantısı sınırları
ALLOWED = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'csv', 'docx', 'xlsx', 'json'}

def allowed_file(fn):
    # Dosya adı içinde '.' ve uzantısı allowed listede mi?
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED

# Flask-Limiter ile rate limiting (IP başına limit)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute"]  # Tüm API için 60 istek/dakika
)

@app.route('/api/convert', methods=['POST'])
@limiter.limit("10 per minute")  # Tek endpointe ekstra limit (opsiyonel)
def api_convert():
    if 'file' not in request.files:
        return jsonify({'error': 'file eksik'}), 400
    f = request.files['file']
    if f.filename == '' or not allowed_file(f.filename):
        return jsonify({'error': 'geçersiz uzantı'}), 400

    fn = secure_filename(f.filename)
    unique = f"{uuid.uuid4().hex}_{fn}"
    in_path = os.path.join(UPLOAD_FOLDER, unique)
    f.save(in_path)

    # Dosya türü kontrolü (magic ile) - ek güvenlik
    try:
        detected_type = magic.from_file(in_path, mime=True)
        logging.info(f"Yüklenen dosya: {fn}, magic_type: {detected_type}")
    except Exception as e:
        detected_type = "Bilinmiyor"
        logging.error(f"Magic check başarısız: {e}")

    try:
        raw = convert_input(in_path)
        parsed = call_llm(raw)
    except Exception as e:
        logging.error(f"Ayrıştırma hatası: {str(e)}")
        return jsonify({'error': str(e)}), 500

    out_name = f"{uuid.uuid4().hex}_{fn.rsplit('.',1)[0]}.xlsx"
    out_path = os.path.join(OUTPUT_FOLDER, out_name)
    try:
        save_as_excel(parsed, out_path)
    except Exception as e:
        logging.error(f"Excel kaydı hatası: {str(e)}")
        return jsonify({'error': str(e)}), 500

    logging.info(f"İşlem tamamlandı: {fn} -> {out_name}")
    return jsonify({'download_url': f"/api/download/{out_name}"}), 200

@app.route('/api/download/<filename>', methods=['GET'])
def api_download(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(path):
        return jsonify({'error': 'bulunamadı'}), 404
    return send_file(path, as_attachment=True)

@app.route('/api/preview', methods=['POST'])
@limiter.limit("20 per minute")
def api_preview():
    if 'file' not in request.files:
        return jsonify({'error': 'file eksik'}), 400
    f = request.files['file']
    if f.filename == '' or not allowed_file(f.filename):
        return jsonify({'error': 'geçersiz uzantı'}), 400

    fn = secure_filename(f.filename)
    unique = f"{uuid.uuid4().hex}_{fn}"
    in_path = os.path.join(UPLOAD_FOLDER, unique)
    f.save(in_path)

    try:
        raw = convert_input(in_path)
        parsed = call_llm(raw)
    except Exception as e:
        logging.error(f"Preview hatası: {str(e)}")
        return jsonify({'error': str(e)}), 500

    return jsonify({'parsed_data': parsed}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
