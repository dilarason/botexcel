# web_ui.py
# Flask web arayüzü: dosya güvenliği, rate limit, logging ve oturum yönetimiyle TAM hali

from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import os, uuid, logging, magic
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from users import db, User
from converter import convert_input
from ai_module import call_llm
from save_to_excel import save_as_excel

# Log klasörü ve loglama ayarı
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "botexcel-secret")

# Database ve Login sistemi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Rate limit
limiter = Limiter(app, key_func=get_remote_address, default_limits=["60 per minute"])

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
ALLOWED = {'pdf', 'txt', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024

# Dosya güvenliği
def is_allowed_file(file_storage):
    filename = file_storage.filename
    if '.' not in filename or filename.rsplit('.',1)[1].lower() not in ALLOWED:
        return False
    file_storage.seek(0, os.SEEK_END)
    file_size = file_storage.tell()
    file_storage.seek(0)
    if file_size > MAX_FILE_SIZE:
        return False
    mime = magic.from_buffer(file_storage.read(2048), mime=True)
    file_storage.seek(0)
    if not (
        mime.startswith("application/pdf") or
        mime.startswith("text/plain") or
        mime.startswith("image/")
    ):
        return False
    return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı, giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Başarıyla giriş yaptınız.', 'success')
            return redirect(url_for('index'))
        else:
            flash('E-posta veya şifre hatalı!', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yaptınız.', 'info')
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")
@login_required
def upload():
    try:
        uploaded_file = request.files.get('file')
        if not uploaded_file or not is_allowed_file(uploaded_file):
            logging.warning("/upload: Dosya türü veya boyutu hatalı")
            flash("Desteklenmeyen dosya türü veya dosya çok büyük!", "danger")
            return redirect(url_for('index'))
        _, ext = os.path.splitext(uploaded_file.filename)
        unique_name = f"{uuid.uuid4()}{ext}"
        input_path = os.path.join(UPLOAD_FOLDER, unique_name)
        uploaded_file.save(input_path)
        logging.info(f"/upload: Dosya kaydedildi: {input_path}")
        try:
            raw = convert_input(input_path)
        except Exception as e:
            logging.error(f"/upload: convert_input hata: {e}", exc_info=True)
            flash("Dosya okunurken hata oluştu.", "danger")
            return redirect(url_for('index'))
        try:
            parsed = call_llm(raw)
        except Exception as e:
            logging.error(f"/upload: call_llm hata: {e}", exc_info=True)
            flash("Yapay zeka ile işlenirken hata oluştu.", "danger")
            return redirect(url_for('index'))
        output_name = f"out_{uuid.uuid4()}.xlsx"
        output_path = os.path.join(OUTPUT_FOLDER, output_name)
        try:
            save_to_excel(parsed, output_path)
        except Exception as e:
            logging.error(f"/upload: save_to_excel hata: {e}", exc_info=True)
            flash("Excel dosyası oluşturulurken hata oluştu.", "danger")
            return redirect(url_for('index'))
        logging.info(f"/upload: Başarıyla tamamlandı, çıktı: {output_path}")
        return redirect(url_for('download', filename=output_name))
    except Exception as e:
        logging.error(f"/upload: Genel hata: {e}", exc_info=True)
        flash("Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.", "danger")
        return redirect(url_for('index'))

@app.route('/download/<filename>', methods=['GET'])
@limiter.limit("30 per minute")
@login_required
def download(filename):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if not os.path.exists(file_path):
            logging.warning(f"/download: Dosya bulunamadı: {filename}")
            flash("İstenen dosya bulunamadı.", "danger")
            return redirect(url_for('index'))
        logging.info(f"/download: Dosya gönderiliyor: {filename}")
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logging.error(f"/download: Hata: {e}", exc_info=True)
        flash("Dosya indirilemedi.", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
