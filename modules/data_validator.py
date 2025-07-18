# modules/data_validator.py
"""
Veri Doğrulama & Anomali Tespit Modülü

Bu modül, Excel-bot-ai projesinin 'Veri Doğrulama & Anomali Tespit' özelliğini sağlar.
Özellikler:
- Boş satır kontrolü
- Hücre türü uyuşmazlığı tespit (örneğin sayı olması gereken yerde metin)
- Tarih formatı doğrulama
- Mantıksal tutarsızlık tespiti (örn. negatif fiyat, toplam != miktar × fiyat)
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any

def detect_empty_rows(df: pd.DataFrame) -> List[int]:
    """Tamamen boş olan satırların indekslerini döner."""
    return [i for i, row in df.iterrows() if row.isnull().all()]


def detect_type_mismatches(df: pd.DataFrame, column_types: Dict[str, type]) -> Dict[str, List[int]]:
    """
    Belirtilen sütun tiplerine uymayan hücrelerin satır indekslerini döner.
    column_types: {'Fiyat': float, 'Tarih': pd.Timestamp}
    """
    mismatches = {}
    for col, expected in column_types.items():
        bad = []
        for i, val in df[col].iteritems():
            if not (isinstance(val, expected) or pd.isna(val)):
                bad.append(i)
        if bad:
            mismatches[col] = bad
    return mismatches


def detect_date_format(df: pd.DataFrame, column: str, date_format: str) -> List[int]:
    """
    Belirli tarih formatına uymayan değerlerin satır indekslerini döner.
    date_format örn: '%Y-%m-%d'
    """
    bad = []
    for i, val in df[column].iteritems():
        try:
            pd.to_datetime(val, format=date_format)
        except:
            bad.append(i)
    return bad


def detect_logical_inconsistencies(df: pd.DataFrame, rules: List[Any]) -> List[int]:
    """
    Mantıksal kurallara uymayan satırları döner.
    Kurallar: liste olarak lambdalı fonksiyonlar veya tuple ('Toplam', lambda row: row['Toplam'] != row['Fiyat']*row['Miktar'])
    """
    bad = []
    for i, row in df.iterrows():
        for rule in rules:
            if isinstance(rule, tuple):
                _, func = rule
                if not func(row):
                    bad.append(i)
            elif callable(rule):
                if not rule(row):
                    bad.append(i)
    return list(set(bad))


def validate_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Tüm doğrulama adımlarını çalıştırır ve özet bir rapor döner.
    """
    report = {}
    empty = detect_empty_rows(df)
    if empty:
        report['empty_rows'] = empty

    # Örnek tip kontrolü
    type_mismatch = detect_type_mismatches(df, {'Fiyat': (int, float), 'Tarih': str})
    if type_mismatch:
        report['type_mismatches'] = type_mismatch

    # Örnek mantıksal tutarsızlık
    inconsistencies = detect_logical_inconsistencies(df, [
        ('Toplam', lambda r: float(r.get('Toplam', 0)) == float(r.get('Fiyat', 0)) * float(r.get('Miktar', 1)))
    ])
    if inconsistencies:
        report['logical_inconsistencies'] = inconsistencies

    return report
