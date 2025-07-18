# modules/multi_format_loader.py
"""
Çoklu Format ve Otomatik Veri Birleştirme Modülü

Bu modül, birden fazla dosya türünü (PDF, JPG, PNG, TXT, CSV)
yükleyip tek bir pandas DataFrame olarak birleştirmeyi sağlar.
Her satıra, kaynağı ifade eden bir 'source' sütunu ekler.
"""
import os
import pandas as pd
from converter import convert_input
from typing import List


def load_and_merge(file_paths: List[str]) -> pd.DataFrame:
    """
    file_paths: liste halinde dosya yolları
    - Her dosya convert_input ile işlenir
    - DataFrame'e dönüştürülür
    - 'source' isimli bir sütun eklenir ve orijinal dosya adını içerir
    - Tüm DataFrame'ler birleştirilir ve döndürülür
    """
    dfs = []
    for path in file_paths:
        # Ham veriyi al
        data = convert_input(path)
        df = pd.DataFrame(data)
        # Kaynak sütunu ekle
        df['source'] = os.path.basename(path)
        dfs.append(df)

    # Tek DataFrame olarak birleştir
    merged = pd.concat(dfs, ignore_index=True, sort=False)
    return merged
