import React from "react";

const badgeMap = {
  rookie: { label: "Yeni Başlayan", emoji: "🌱" },
  // Gelecekte başka rozetler de ekleyebilirsin
};

export default function ProfileCard({ profile }) {
  if (!profile) return null;

  const { email, xp, level, badges } = profile;
  const nextLevelXp = (level) * 100;
  const prevLevelXp = (level - 1) * 100;
  const levelProgress = Math.min(100, Math.round(((xp - prevLevelXp) / 100) * 100));

  return (
    <div className="rounded-3xl shadow-xl bg-white/80 p-6 flex flex-col gap-3 w-full max-w-md mx-auto border border-[#d6ede2]">
      <div className="flex items-center gap-4">
        <div className="bg-[#217346] text-white w-14 h-14 rounded-full flex items-center justify-center text-3xl font-bold shadow">
          {email[0]?.toUpperCase() || "U"}
        </div>
        <div>
          <div className="font-bold text-[#217346] text-lg truncate">{email}</div>
          <div className="flex gap-2 items-center mt-1">
            <span className="bg-[#e5fff1] px-3 py-1 rounded-lg text-[#217346] font-semibold text-sm shadow">
              Seviye {level}
            </span>
            <span className="text-xs text-gray-400">{xp} XP</span>
          </div>
        </div>
      </div>
      {/* XP Barı */}
      <div className="mt-2">
        <div className="w-full bg-gray-200 rounded-full h-3 relative">
          <div
            className="bg-gradient-to-r from-[#217346] to-[#45ce7b] h-3 rounded-full shadow transition-all"
            style={{ width: `${levelProgress}%` }}
          />
          <span className="absolute left-1/2 -top-7 text-xs text-gray-400" style={{ transform: "translateX(-50%)" }}>
            {xp - prevLevelXp} / 100 XP
          </span>
        </div>
      </div>
      {/* Rozetler */}
      <div className="flex gap-2 mt-3 flex-wrap">
        {badges?.filter(b=>b).length > 0 ? badges.filter(b=>b).map((b, i) =>
          <span
            key={b}
            className="flex items-center gap-1 bg-[#e9fbe8] border border-[#b7e2c6] text-[#19944e] rounded-xl px-3 py-1 text-sm font-semibold shadow-sm"
          >
            <span>{badgeMap[b]?.emoji || "🏅"}</span>
            <span>{badgeMap[b]?.label || b}</span>
          </span>
        ) : (
          <span className="italic text-gray-400 text-xs">Henüz rozetin yok</span>
        )}
      </div>
    </div>
  );
}
