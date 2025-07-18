# modules/template_suggester.py
"""
Otomatik Şablon/Format Çıkartıcı Modülü

Bu modül, verilen DataFrame'in yapısına bakarak en uygun Excel şablonunu önerir.
Örnek şablonlar: 'invoice', 'inventory', 'sales_report', 'stock_register'
"""
import pandas as pd
from typing import List

# Örnek şablon kriterleri
TEMPLATES = {
    'invoice': ['invoice_no', 'date', 'customer', 'amount'],
    'inventory': ['item', 'quantity', 'location'],
    'sales_report': ['product', 'units_sold', 'revenue'],
    'stock_register': ['item_code', 'stock_level', 'reorder_point']
}


def suggest_template(df: pd.DataFrame) -> List[str]:
    """
    DataFrame sütunlarını TEMPLATES anahtarlarıyla karşılaştırır.
    En fazla eşleşen sütuna sahip şablonları listeler.
    Return: en uygun şablon isimleri
    """
    cols = set(df.columns)
    scores = {}
    for template, required in TEMPLATES.items():
        match_count = len(cols.intersection(required))
        scores[template] = match_count
    # En yüksek skoru bul
    max_score = max(scores.values())
    # Eşleşme sayısı 0 ise öneri yok
    if max_score == 0:
        return []
    # En iyi şablonları döndür
    return [t for t, s in scores.items() if s == max_score]
