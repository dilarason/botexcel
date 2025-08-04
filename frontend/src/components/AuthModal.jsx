import React, { useState } from "react";
import axios from "axios";

export default function AuthModal({ isOpen, onClose, onAuth }) {
  const [mode, setMode] = useState("login"); // "login" veya "register"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      const url = mode === "login" ? "/api/login" : "/api/register";
      const { data } = await axios.post(url, { email, password });
      if (mode === "login" && data.access_token) {
        setMsg("Başarılı giriş!");
        onAuth(data.access_token);
        onClose();
      } else if (mode === "register" && !data.error) {
        setMsg("Kayıt başarılı! Giriş yapabilirsiniz.");
        setMode("login");
      } else {
        setMsg(data.message || "Bilinmeyen hata!");
      }
    } catch (err) {
      setMsg(err.response?.data?.message || "Hata oluştu!");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-black/40">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md relative">
        <button onClick={onClose} className="absolute top-2 right-3 text-xl text-gray-400 hover:text-red-600">&times;</button>
        <h2 className="text-2xl font-bold text-[#217346] mb-2">
          {mode === "login" ? "Giriş Yap" : "Kayıt Ol"}
        </h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-2">
          <input
            className="rounded px-4 py-2 border border-gray-300"
            placeholder="E-posta"
            type="email"
            autoFocus
            required
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
          <input
            className="rounded px-4 py-2 border border-gray-300"
            placeholder="Şifre"
            type="password"
            required
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
          <button className="bg-[#217346] text-white rounded-xl py-2 font-bold hover:bg-[#155939] transition">
            {mode === "login" ? "Giriş Yap" : "Kayıt Ol"}
          </button>
          {msg && <div className="text-center text-sm text-red-500">{msg}</div>}
        </form>
        <div className="mt-4 text-center">
          {mode === "login"
            ? (
              <span>
                Hesabın yok mu?{" "}
                <button className="text-[#217346] underline" onClick={() => setMode("register")}>Kayıt Ol</button>
              </span>
            ) : (
              <span>
                Zaten hesabın var mı?{" "}
                <button className="text-[#217346] underline" onClick={() => setMode("login")}>Giriş Yap</button>
              </span>
            )}
        </div>
      </div>
    </div>
  );
}
