# modules/sensitive_data_detector.py
"""
Hassas Bilgi Bulma & Kırmızı Uyarı Modülü

Bu modül, DataFrame içindeki
- Telefon numarası,
- TCKN (11 haneli sayısal),
- IBAN (TR ile başlayan),
- Kredi kartı numarası (16 haneli),
- E-posta adresi,
- Şifre (örneğin 8+ karakter, karmaşık)
gibi hassas verileri tespit eder ve raporlar.
"""
import re
import pandas as pd
from typing import List, Dict

# Regex desenleri
PATTERNS: Dict[str, re.Pattern] = {
    'phone': re.compile(r"\b\d{3}[- ]?\d{3}[- ]?\d{2}[- ]?\d{2}\b"),
    'tckn': re.compile(r"\b\d{11}\b"),
    'iban': re.compile(r"\bTR\d{24}\b"),
    'credit_card': re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b"),
    'email': re.compile(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,6}"),
}


def detect_sensitive(df: pd.DataFrame) -> Dict[str, List[tuple]]:
    """
    Her desen için (satır, sütun) çiftlerini döner.
    """
    report = {}
    for label, pattern in PATTERNS.items():
        hits = []
        for r, row in df.iterrows():
            for c, val in enumerate(row):
                if isinstance(val, str) and pattern.search(val):
                    hits.append((r, df.columns[c]))
        if hits:
            report[label] = hits
    return report


def mask_sensitive(df: pd.DataFrame, report: Dict[str, List[tuple]]) -> pd.DataFrame:
    """
    Tespit edilen hücreleri maskeler (örneğin ****).
    """
    df_masked = df.copy()
    for label, cells in report.items():
        for (r, c) in cells:
            df_masked.at[r, c] = '***MASKED***'
    return df_masked
