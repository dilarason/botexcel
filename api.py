# api.py
# 🔹 JWT ile korunan, ayrıntılı hata yanıtı veren REST API (kayıt, giriş, convert, history...)

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import logging
import magic  # Dosya türü kontrolü
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import datetime

from users import db, User
from converter import convert_input
from ai_module import call_llm
from save_to_excel import save_as_excel

# --------------- KÜÇÜK GEÇMİŞ MODELI ---------------
from flask_sqlalchemy import SQLAlchemy
class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    out_filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(32), default="success")

# --------------- UYGULAMA ve LOG AYARLARI ---------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "botexcel-jwt-secret")

db.init_app(app)
jwt = JWTManager(app)

# -- YENİ FLASK-LIMITER BAŞLANGICI! --
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60 per minute"]
)
limiter.init_app(app)
# -- ESKİ "Limiter(app, ...)" KULLANIMINI KESİNLİKLE KALDIR! --

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ALLOWED = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'csv', 'docx', 'xlsx', 'json'}

def allowed_file(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED

# --------------- KULLANICI KAYDI (REGISTER) ---------------
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "error": True,
            "code": "MISSING_FIELDS",
            "message": "Email ve şifre gereklidir."
        }), 400

    if User.query.filter_by(email=email).first():
        return jsonify({
            "error": True,
            "code": "EMAIL_EXISTS",
            "message": "Bu e-posta zaten kayıtlı."
        }), 409

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "error": False,
        "message": "Kayıt başarılı. Giriş yapabilirsiniz."
    }), 201

# --------------- KULLANICI GİRİŞİ (LOGIN) + JWT ÜRETİMİ ---------------
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "error": True,
            "code": "MISSING_FIELDS",
            "message": "Email ve şifre gereklidir."
        }), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({
            "error": True,
            "code": "AUTH_FAILED",
            "message": "E-posta veya şifre hatalı."
        }), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "error": False,
        "access_token": access_token
    }), 200

# --------------- DOSYA DÖNÜŞTÜRME (PROTECTED) ---------------
@app.route('/api/convert', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def api_convert():
    user_id = get_jwt_identity()
    if 'file' not in request.files:
        return jsonify({
            "error": True,
            "code": "NO_FILE",
            "message": "Dosya eksik."
        }), 400
    f = request.files['file']
    if f.filename == '' or not allowed_file(f.filename):
        return jsonify({
            "error": True,
            "code": "INVALID_EXT",
            "message": "Geçersiz dosya uzantısı."
        }), 400

    fn = secure_filename(f.filename)
    unique = f"{uuid.uuid4().hex}_{fn}"
    in_path = os.path.join(UPLOAD_FOLDER, unique)
    f.save(in_path)
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
        return jsonify({
            "error": True,
            "code": "PARSE_ERROR",
            "message": str(e)
        }), 500

    out_name = f"{uuid.uuid4().hex}_{fn.rsplit('.',1)[0]}.xlsx"
    out_path = os.path.join(OUTPUT_FOLDER, out_name)
    try:
        save_as_excel(parsed, out_path)
    except Exception as e:
        logging.error(f"Excel kaydı hatası: {str(e)}")
        return jsonify({
            "error": True,
            "code": "EXCEL_ERROR",
            "message": str(e)
        }), 500

    # KULLANICI GEÇMİŞİNE KAYDET
    try:
        hist = UserHistory(
            user_id=user_id,
            filename=fn,
            out_filename=out_name,
            status="success"
        )
        db.session.add(hist)
        db.session.commit()
    except Exception as e:
        logging.error(f"History kaydı hatası: {str(e)}")

    # ----------- OYUNLAŞTIRMA: XP, LEVEL, BADGE GÜNCELLEME ------------
    try:
        user = User.query.get(user_id)
        user.xp = (user.xp or 0) + 10
        user.level = (user.xp // 100) + 1
        if user.xp >= 50 and "rookie" not in (user.badges or ""):
            user.badges = (user.badges or "") + ",rookie"
        db.session.commit()
    except Exception as e:
        logging.error(f"XP/level update failed: {str(e)}")

    return jsonify({
        "error": False,
        "download_url": f"/api/download/{out_name}"
    }), 200

# --------------- DOSYA İNDİRME (PROTECTED) ---------------
@app.route('/api/download/<filename>', methods=['GET'])
@jwt_required()
@limiter.limit("30 per minute")
def api_download(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(path):
        return jsonify({
            "error": True,
            "code": "NOT_FOUND",
            "message": "İstenen dosya bulunamadı."
        }), 404
    return send_file(path, as_attachment=True)

# --------------- KULLANICI GEÇMİŞİ (PROTECTED) ---------------
@app.route('/api/history', methods=['GET'])
@jwt_required()
def api_history():
    user_id = get_jwt_identity()
    # Son 30 işlemi yeniye göre sırala
    q = UserHistory.query.filter_by(user_id=user_id).order_by(UserHistory.created_at.desc()).limit(30)
    result = []
    for h in q:
        result.append({
            "id": h.id,
            "filename": h.filename,
            "download_url": f"/api/download/{h.out_filename}",
            "created_at": h.created_at.isoformat(sep=" ", timespec="seconds"),
            "status": h.status
        })
    return jsonify({
        "error": False,
        "history": result
    }), 200

# --------------- UYGULAMA BAŞLATICI ---------------
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def api_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": True, "message": "Kullanıcı bulunamadı."}), 404
    return jsonify({
        "error": False,
        "email": user.email,
        "xp": user.xp or 0,
        "level": user.level or 1,
        "badges": (user.badges or "").strip(",").split(",") if user.badges else [],
    }), 200
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
