from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os

from converter import convert_input
from save_to_excel import save_as_excel

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            print("❌ Dosya gelmedi.")
            return "Dosya yüklenemedi.", 400
        
        uploaded_file = request.files["file"]
        
        if uploaded_file.filename == "":
            print("❌ Dosya adı boş.")
            return "Dosya seçilmedi.", 400

        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(file_path)

        # Dönüştür
        structured_data = convert_input(file_path)

        # Excel'e kaydet
        output_path = os.path.join(OUTPUT_FOLDER, "output.xlsx")
        save_as_excel(structured_data, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


@app.route("/demo", methods=["GET", "POST"])
def demo():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file or uploaded_file.filename == "":
            return "Demo için dosya gerekli.", 400

        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(file_path)

        structured_data = convert_input(file_path)
        output_path = os.path.join(OUTPUT_FOLDER, "demo_output.xlsx")
        save_as_excel(structured_data, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("demo.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username") or request.form.get("new_username")
        email = request.form.get("email") or "Yok"
        print(f"🟢 Giriş/Kayıt Denemesi: {username} ({email})")
    return render_template("login.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        print(f"📨 Mesaj alındı: {name} ({email}) → {message}")
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/botexcel-ai")
def botexcel_ai():
    return render_template("botexcel-ai.html")


if __name__ == "__main__":
    app.run(debug=True)
