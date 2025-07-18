import React from "react";

export default function DemoMode() {
  return (
    <button
      className="bg-green-500 text-white px-6 py-2 rounded-xl"
      onClick={() => alert("Demo Modu açılıyor... (ileride eklenecek)")}
    >
      Demo Modu
    </button>
  );
}
