# ai_module.py
# 🔹 BotExcel.AI - GGUF formatlı yerel modelle (llama-cpp-python) entegre

from llama_cpp import Llama        # GGUF modelini çalıştırmak için
import json                        # JSON ayrıştırma
import os                          # Dosya yol işlemleri
import re                          # JSON blok ayıklamak için

# 📍 Model dosyasının tam yolu
MODEL_PATH = os.path.expanduser("~/Masaüstü/nous-hermes-2-mistral-7b-dpo.Q4_0.gguf")

# 🚀 Modeli yükle
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,             # Konteks uzunluğu (token sayısı)
    n_threads=3,            # CPU: i5-7200U için en iyi ayar
    verbose=True            # Logları göster
)

# 🔁 Ana AI fonksiyonu
def call_llm(raw_list):
    """
    Ham veri listesini alır, prompt ile modele yollar,
    JSON çıktısını döndürür.
    """
    # 🧠 Açık ve anlaşılır prompt
    prompt = (
        "Sen BotExcel.AI’sın. Elindeki listeyi al, her satırı ayrıştır ve "
        "JSON formatında (Key, Value, Type, Notes) olarak geri döndür.\n\n"
        f"Input: {json.dumps(raw_list, ensure_ascii=False)}\nOutput:"
    )

    # 📨 AI'a gönder
    response = llm(
        prompt,
        max_tokens=1024,
        temperature=0.2,
        stop=["</s>", "Input:"]
    )

    # 📤 Modelin cevabı
    text = response["choices"][0]["text"]

    # 🧼 JSON bloğunu güvenli ayıkla
    match = re.search(r"\[\s*{.*?}\s*]", text, re.DOTALL)
    if not match:
        raise RuntimeError(f"❌ JSON bulunamadı.\nYanıt:\n{text}")
    json_part = match.group(0)

    # 🧪 JSON parse
    try:
        return json.loads(json_part)
    except Exception as e:
        raise RuntimeError(f"❌ JSON ayrıştırma hatası: {e}\n🔎 JSON Bölüm:\n{json_part}")

# 🧪 Test çalıştırması (doğrudan dosya çalıştırılırsa)
if __name__ == "__main__":
    örnek = ["Adı: Ahmet", "Soyadı: Demir", "Tarih: 2023-05-10"]
    çıktı = call_llm(örnek)
    print("✅ AI çıktısı:\n", json.dumps(çıktı, indent=2, ensure_ascii=False))
