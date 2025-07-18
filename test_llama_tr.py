from llama_cpp import Llama

llm = Llama(
    model_path="/home/ted/Indirilenler/Turkish-Llama-8b-Instruct-v0.1.Q6_K.gguf",
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=0
)

prompt = """
Senin adın BotExcel. Bir Türkçe Excel AI'sın. Sana verilen satır listesini aşağıdaki kurallara göre işle:

1. Her satırı ayrı bir tablo kaydına çevir.
2. Her kayıt şu şekilde olmalı: {"Key": ..., "Value": ..., "Type": ..., "Notes": ...}
   - "Key": Satırdaki başlık (ör: Adı, Soyadı, Fatura No, BARCODE, vb.)
   - "Value": Satırdaki değer (ör: Ahmet, 12345, vs.)
   - "Type": Bu verinin tipi (ör: Kişi, Barkod, Tutar, Tarih, Ürün, Açıklama, vb.)
   - "Notes": Varsayılan boş bırak, ek bilgi varsa yaz.
3. Sadece geçerli JSON formatında bir Python listesi döndür. Ek açıklama, yorum, açıklayıcı metin, formül veya başka bir şey ekleme.
4. Sadece listeyi döndür, başka hiçbir şey yazma.

Input: ["Adı: Ahmet", "BARCODE: 12345"]

Output:
"""

output = llm(prompt, max_tokens=256)
print(output["choices"][0]["text"])
