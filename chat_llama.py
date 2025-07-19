from llama_cpp import Llama
import os

MODEL_PATH = os.path.expanduser('~/Masaüstü/mistral-7b-instruct-v0.2.Q4_0 (1).gguf')

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=3,
    verbose=False
)

def chat_loop():
    print("💬 BotExcel.AI terminaline hoş geldin. Çıkmak için 'çık' yaz.\n")
    while True:
        user_input = input("👤 Sen: ").strip()
        if user_input.lower() in ["çık", "exit", "quit"]:
            print("👋 Görüşmek üzere!")
            break
        prompt = f"Kullanıcı: {user_input}\nBot:"
        response = llm(
            prompt,
            max_tokens=128,
            temperature=0.7,
            stop=["\nKullanıcı:"]
        )
        text = response["choices"][0]["text"].strip()
        print(f"🤖 BotExcel: {text}\n")

if __name__ == "__main__":
    chat_loop()
