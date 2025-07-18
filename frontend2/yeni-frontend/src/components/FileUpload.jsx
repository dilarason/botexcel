import React, { useRef } from "react";

export default function FileUpload() {
  const inputRef = useRef();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      alert("Dosya seçildi: " + file.name);
      // Sonraki adımda: API'ye yükleme eklenecek.
    }
  };

  return (
    <div className="flex flex-col items-center">
      <input
        type="file"
        ref={inputRef}
        className="hidden"
        onChange={handleFileChange}
        accept=".pdf,.jpg,.jpeg,.png,.txt"
      />
      <button
        className="bg-blue-500 text-white px-6 py-2 rounded-xl"
        onClick={() => inputRef.current.click()}
      >
        Dosya Yükle
      </button>
    </div>
  );
}
