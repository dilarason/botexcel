# web_ui.py

# 🔹 Flask kütüphanesini içe aktar
from flask import Flask, render_template, request, send_file
import os

# 🔹 Dönüştürme modüllerini içe aktar
from converter import convert_input
from save_to_excel import save_as_excel

# 🔹 Flask uygulamasını başlat (static klasörünü açıkça tanımla!)
app = Flask(__name__, static_folder="static")

# 🔹 Dosya yükleme klasörünü tanımla
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔹 Ana sayfa (form + demo HTML) rotası
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Kullanıcıdan gelen dosyayı al
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            # Yüklenen dosyayı uploads klasörüne kaydet
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Dosyayı uygun formata göre işleyip yapılandırılmış veri çıkar
            structured_data = convert_input(file_path)

            # Excel çıktısını oluştur ve kaydet
            output_path = "output/output.xlsx"
            save_as_excel(structured_data, output_path)

            # Kullanıcıya Excel dosyasını indirmesi için gönder
            return send_file(output_path, as_attachment=True)

    # GET isteğiyle sayfa yüklendiğinde index.html göster
    return render_template("index.html")

# 🔹 Flask sunucusunu başlat
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

