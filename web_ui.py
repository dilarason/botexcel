# web_ui.py
# Flask web arayüzü: format seçimi, dosya güvenliği, kullanıcı giriş/çıkışı dahil

from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import os, uuid, logging, magic
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from users import db, User
from converter import convert_input
from ai_module import call_llm
from save_to_excel import save_as_excel

# Log ayarı
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "botexcel-secret")

# DB ve login
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["60 per minute"])
limiter.init_app(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED = {'pdf', 'txt', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def is_allowed_file(file_storage):
    filename = file_storage.filename
    if '.' not in filename or filename.rsplit('.',1)[1].lower() not in ALLOWED:
        return False
    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)
    if size > MAX_FILE_SIZE:
        return False
    mime = magic.from_buffer(file_storage.read(2048), mime=True)
    file_storage.seek(0)
    return mime.startswith("application/pdf") or mime.startswith("text/plain") or mime.startswith("image/")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash("Bu e-posta zaten kayıtlı!", "danger")
            return redirect(url_for('register'))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Kayıt başarılı, giriş yapabilirsiniz.", "success")
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
            flash("Giriş başarılı.", "success")
            return redirect(url_for('index'))
        flash("E-posta veya şifre hatalı!", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")
@login_required
def upload():
    try:
        uploaded_file = request.files.get('file')
        template = request.form.get("format", "klasik")

        if not uploaded_file or not is_allowed_file(uploaded_file):
            logging.warning("❌ Desteklenmeyen dosya türü")
            flash("Desteklenmeyen dosya türü!", "danger")
            return redirect(url_for('index'))

        _, ext = os.path.splitext(uploaded_file.filename)
        unique_name = f"{uuid.uuid4()}{ext}"
        input_path = os.path.join(UPLOAD_FOLDER, unique_name)
        uploaded_file.save(input_path)
        logging.info(f"✅ Dosya yüklendi: {input_path}")

        raw = convert_input(input_path)
        parsed = call_llm(raw)

        output_name = f"{uuid.uuid4()}.xlsx"
        output_path = os.path.join(OUTPUT_FOLDER, output_name)

        save_to_excel(parsed, output_path)  # template doğrudan `save_to_excel.py` içine entegre edilmeli

        logging.info(f"💾 Çıktı oluşturuldu: {output_path}")
        return redirect(url_for('download', filename=output_name))

    except Exception as e:
        logging.error(f"Hata /upload: {e}", exc_info=True)
        flash("Bir hata oluştu, lütfen tekrar deneyin.", "danger")
        return redirect(url_for('index'))

@app.route('/download/<filename>')
@limiter.limit("30 per minute")
@login_required
def download(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(path):
        flash("Dosya bulunamadı!", "danger")
        return redirect(url_for('index'))
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
