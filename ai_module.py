# ai_module.py
# 🔹 BotExcel AI: transformers + bitsandbytes ile Vicuna-7B–HF entegrasyonu (Lazy yükleme)

import json
import threading
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
import torch

# 4-bit quant config (global olarak tanımlı)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

# Model ve tokenizer küresel değişkenler, başlangıçta None
_model = None
_tokenizer = None
# Thread güvenliği için kilit
_lock = threading.Lock()


def _load_model():
    """
    Model ve tokenizer'ı yalnızca bir kez yükler (lazy init).
    """
    global _model, _tokenizer
    with _lock:
        if _model is None or _tokenizer is None:
            MODEL_ID = "TheBloke/vicuna-7B-1.1-HF"
            # slow tokenizer ile yükle (hata önlemek için)
            _tokenizer = AutoTokenizer.from_pretrained(
                MODEL_ID,
                use_fast=False,
                trust_remote_code=True
            )
            _model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )


def call_llm(raw_list):
    # Hızlı test için, AI’yı tamamen bypass et.
    print("!!! TEST MODU: LLM devre dışı !!!")
    # Ham veri ne olursa olsun, örnek bir dict listesi dön.
    return [
        {"Key": "TestKey1", "Value": "TestValue1", "Type": "TypeA", "Notes": "Not1"},
        {"Key": "TestKey2", "Value": "TestValue2", "Type": "TypeB", "Notes": "Not2"}
    ]

    # Modeli ilk çağrıda yükle
    if _model is None or _tokenizer is None:
        _load_model()

    # Prompt şablonu
    prompt = (
        "Sen BotExcel AI’sın. Elindeki ham listeyi (Python listesi) al, "
        "her satırı kurallara göre ayrıştır ve JSON liste olarak döndür.\n\n"
        f"Input: {json.dumps(raw_list, ensure_ascii=False)}\nOutput:"
    )

    # Tokenize ve modele gönder
    inputs = _tokenizer(prompt, return_tensors="pt").to(_model.device)
    outputs = _model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.2,
        do_sample=False
    )

    # Decode
    text = _tokenizer.decode(outputs[0], skip_special_tokens=True)

    # JSON parse
    try:
        json_part = text.split("Output:")[-1].strip()
        parsed = json.loads(json_part)
    except Exception as e:
        raise RuntimeError(f"LLM yanıtı JSON parse edilirken hata: {e}\n{text}")

    return parsed

# 🔹 Test fonksiyonu
if __name__ == "__main__":
    sample = ["Adı: Ahmet", "BARCODE: 12345"]
    print(call_llm(sample))

