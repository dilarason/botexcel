import React from "react";
import api from "../api";

export default function HistoryTable({ history }) {
  if (!history || history.length === 0) {
    return (
      <div className="py-6 text-gray-400 text-center italic border rounded-xl bg-white/70">
        Hiç işlem yapılmadı.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto border rounded-2xl shadow-lg bg-white/90">
      <table className="min-w-full text-sm text-left">
        <thead>
          <tr className="bg-[#f6fbf7]">
            <th className="px-4 py-3 font-bold text-[#217346]">Tarih</th>
            <th className="px-4 py-3 font-bold text-[#217346]">Dosya Adı</th>
            <th className="px-4 py-3 font-bold text-[#217346]">Durum</th>
            <th className="px-4 py-3 font-bold text-[#217346]">Çıktı</th>
          </tr>
        </thead>
        <tbody>
          {history.map(item => (
            <tr key={item.id} className="even:bg-[#f8fefb]">
              <td className="px-4 py-2">{item.created_at?.split(" ")[0]}</td>
              <td className="px-4 py-2">{item.filename}</td>
              <td className="px-4 py-2">
                {item.status === "success"
                  ? <span className="text-green-700 font-semibold">✓ Başarılı</span>
                  : <span className="text-red-700 font-semibold">Hatalı</span>}
              </td>
              <td className="px-4 py-2">
                {item.download_url ? (
                  <a
                    href={api.defaults.baseURL + item.download_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[#217346] underline font-bold hover:text-[#19944e]"
                  >
                    İndir
                  </a>
                ) : (
                  <span className="text-gray-400">-</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
