from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # --- Oyunlaştırma Alanları ---
    xp = db.Column(db.Integer, default=0)               # Kullanıcı puanı
    level = db.Column(db.Integer, default=1)            # Kullanıcı seviyesi
    badges = db.Column(db.String(255), default="")      # Kazanılan rozetler (virgülle ayrılmış)

    def set_password(self, password):
        """Parolayı hashleyip kaydeder."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Girilen parolayı kontrol eder."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'
