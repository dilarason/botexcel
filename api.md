# BotExcel.AI — API Kullanım Kılavuzu

## 1. `/api/convert` — Dosya Yükle ve Excel'e Dönüştür

**POST /api/convert**

- PDF, TXT, JPG, PNG, CSV, DOCX, XLSX veya JSON dosyanı yükle.
- AI ayrıştırması ile otomatik Excel çıktısı indir.

### İstek Parametreleri

- `file` — zorunlu, dosya (multipart/form-data)
- (Opsiyonel parametreler ileride eklenebilir)

### Örnek cURL isteği

```bash
curl -X POST "http://localhost:5000/api/convert" \
  -F "file=@fatura1.pdf"
