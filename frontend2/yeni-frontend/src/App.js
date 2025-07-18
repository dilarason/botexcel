import React from "react";
import FileUpload from "./components/FileUpload";
import DemoMode from "./components/DemoMode";
// PlusMode henüz yoksa alttaki satırı yorumda bırakabilirsin
// import PlusMode from "./components/PlusMode";

function PlusMode() {
  return (
    <button className="bg-yellow-500 text-white px-6 py-2 rounded-xl">
      BotExcel Plus
    </button>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-200 flex flex-col">
      {/* ÜST BAR: LOGO ve Başlık */}
      <header className="p-6 flex items-center justify-between shadow-lg">
        <img src="/logo.svg" alt="BotExcel Logo" className="h-12" />
        <h1 className="text-3xl font-extrabold text-blue-900 tracking-wide">BotExcel.Ai</h1>
        <button className="bg-blue-500 text-white px-4 py-2 rounded-lg">Giriş Yap</button>
      </header>

      {/* ORTA GRID: 4 Kutu */}
      <main className="flex-1 flex flex-col items-center justify-center">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 p-4">
          <div className="bg-white rounded-2xl shadow-xl flex flex-col items-center p-6 hover:scale-105 transition">
            <FileUpload />
          </div>
          <div className="bg-white rounded-2xl shadow-xl flex flex-col items-center p-6 hover:scale-105 transition">
            <DemoMode />
          </div>
          <div className="bg-white rounded-2xl shadow-xl flex flex-col items-center p-6 hover:scale-105 transition">
            <PlusMode />
          </div>
          <div className="bg-white rounded-2xl shadow-xl flex flex-col items-center p-6 hover:scale-105 transition">
            <a href="#about" className="text-blue-700 font-bold text-lg">Hakkımızda</a>
          </div>
        </div>
        {/* ALTTA DESTEKLENEN FORMAT İKONLARI */}
        <div className="flex gap-8 mt-12">
          <img src="/icons/pdf.svg" alt="PDF" className="h-10" />
          <img src="/icons/image.svg" alt="Görsel" className="h-10" />
          <img src="/icons/ocr.svg" alt="OCR" className="h-10" />
          <img src="/icons/txt.svg" alt="TXT" className="h-10" />
        </div>
        {/* Footer */}
        <footer className="text-center text-gray-400 p-4 text-xs w-full mt-8">
          BotExcel © {new Date().getFullYear()} | MIT Lisansı
        </footer>
      </main>
    </div>
  );
}
