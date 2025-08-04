import React, { useState, useEffect } from "react";
import AuthModal from "./components/AuthModal";
import GameOfDay from "./components/GameOfDay";
import logo from "./assets/logo.svg";
import api from "./api";
import HistoryTable from "./components/HistoryTable";
import ProfileCard from "./components/ProfileCard";

export default function App() {
  const [authOpen, setAuthOpen] = useState(false);
  const [token, setToken] = useState(() => localStorage.getItem("token") || null);
  const [file, setFile] = useState(null);
  const [uploadMsg, setUploadMsg] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");
  const [gecmis, setGecmis] = useState([]);
  const [profile, setProfile] = useState(null);

  // Girişte ve her yüklemede geçmiş ve profil bilgisi çek
  useEffect(() => {
    if (token) {
      fetchHistory();
      fetchProfile();
    } else {
      setGecmis([]);
      setProfile(null);
    }
  }, [token]);

  // Geçmiş işlemleri çek
  const fetchHistory = async () => {
    try {
      const { data } = await api.get("/api/history");
      if (!data.error && Array.isArray(data.history)) {
        setGecmis(data.history);
      }
    } catch {
      setGecmis([]);
    }
  };

  // Profil bilgisi çek
  const fetchProfile = async () => {
    try {
      const { data } = await api.get("/api/profile");
      if (!data.error) setProfile(data);
    } catch {
      setProfile(null);
    }
  };

  // Auth
  const handleAuth = (jwt) => {
    setToken(jwt);
    localStorage.setItem("token", jwt);
  };
  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("token");
    setFile(null);
    setUploadMsg("");
    setDownloadUrl("");
    setGecmis([]);
    setProfile(null);
  };
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadMsg("");
    setDownloadUrl("");
  };

  // Dosya yükle
  const handleUpload = async () => {
    if (!file) {
      setUploadMsg("Lütfen bir dosya seçin!");
      return;
    }
    setUploadMsg("Yükleniyor...");
    setDownloadUrl("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const { data } = await api.post("/api/convert", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      if (!data.error && data.download_url) {
        setUploadMsg("Başarılı! Çıktı dosyasını indirebilirsiniz.");
        setDownloadUrl(api.defaults.baseURL + data.download_url);
        fetchHistory(); // Listeyi güncelle
        fetchProfile(); // Profil güncelle
      } else {
        setUploadMsg(data.message || "İşlem başarısız!");
      }
    } catch (err) {
      setUploadMsg(err.response?.data?.message || "Hata oluştu!");
    }
  };

  // Arayüz
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#dbefff] via-[#f3faf8] to-[#e2ffe9] flex flex-col font-sans">
      <AuthModal isOpen={authOpen} onClose={() => setAuthOpen(false)} onAuth={handleAuth} />
      {/* Üst Bar */}
      <header className="flex items-center px-8 py-4 bg-white/80 shadow z-10">
        <img src={logo} alt="BotExcel" className="w-14 h-14 mr-4" />
        <span className="text-3xl font-bold text-[#217346] tracking-wide">BotExcel.AI</span>
        <div className="ml-auto flex gap-4">
          {!token && (
            <button
              className="bg-[#217346] text-white px-4 py-2 rounded-2xl shadow hover:bg-[#166e3c] font-bold"
              onClick={() => setAuthOpen(true)}
            >
              Giriş / Kayıt
            </button>
          )}
          {token && (
            <button
              className="bg-gray-200 text-gray-800 px-4 py-2 rounded-2xl shadow font-bold hover:bg-gray-300"
              onClick={handleLogout}
            >
              Çıkış Yap
            </button>
          )}
        </div>
      </header>
      {/* Profil Kartı */}
      {token && profile && (
        <div className="my-8">
          <ProfileCard profile={profile} />
        </div>
      )}
      {/* Ana Blok */}
      <main className="flex flex-1 flex-col lg:flex-row gap-8 p-10 items-center justify-center">
        {/* Sol Kutu: Upload/Demo */}
        <section className="flex flex-col gap-6 bg-white/70 rounded-3xl shadow-xl p-8 max-w-md w-full">
          <h2 className="text-2xl font-bold text-[#217346]">Excel'e Dönüştür</h2>
          <input
            type="file"
            className="mb-2"
            onChange={handleFileChange}
            disabled={!token}
          />
          <button
            className="bg-[#217346] text-white px-6 py-2 rounded-xl font-bold shadow hover:bg-[#176e3d] transition"
            onClick={handleUpload}
            disabled={!token}
          >
            Yükle ve Dönüştür
          </button>
          {uploadMsg && (
            <div className="mt-2 text-center text-base font-mono text-[#217346] bg-[#e9ffe7] rounded-xl p-2 shadow">
              {uploadMsg}
              {downloadUrl && (
                <div>
                  <a
                    href={downloadUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block mt-1 text-[#217346] font-bold underline"
                  >
                    Çıktıyı indir
                  </a>
                </div>
              )}
            </div>
          )}
          <GameOfDay />
        </section>
        {/* Sağ Kutu: Son İşlemler (Modern Tablo) */}
        <section className="flex flex-col gap-6 bg-white/70 rounded-3xl shadow-xl p-8 max-w-2xl w-full">
          <h2 className="text-2xl font-bold text-[#217346]">Son İşlemler</h2>
          <HistoryTable history={gecmis} />
        </section>
      </main>
      {/* Footer */}
      <footer className="text-center text-gray-400 text-sm py-4">
        © {new Date().getFullYear()} BotExcel.AI | Tüm hakları saklıdır.
      </footer>
    </div>
  );
}
