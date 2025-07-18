import re
import pandas as pd
from typing import Callable, Dict

COMMAND_MAP: Dict[str, Callable] = {}

def translate_headers(language: str, df: pd.DataFrame) -> pd.DataFrame:
    translations = {
        'en': {'Ad': 'Name', 'Fiyat': 'Price', 'Tarih': 'Date'},
        'tr': {'Name': 'Ad', 'Price': 'Fiyat', 'Date': 'Tarih'}
    }
    return df.rename(columns=translations.get(language.lower(), {}))

def move_column(column_name: str, position: int, df: pd.DataFrame) -> pd.DataFrame:
    cols = list(df.columns)
    cols.insert(position, cols.pop(cols.index(column_name)))
    return df[cols]

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()

def register_command(pattern: str):
    def decorator(func: Callable):
        COMMAND_MAP[pattern] = func
        return func
    return decorator

@register_command(r"başlıkları (\\w+) yap")
def cmd_translate(match, df: pd.DataFrame) -> pd.DataFrame:
    return translate_headers(match.group(1), df)

@register_command(r"fiyat sütununu ilk sıraya al")
def cmd_move_price_first(match, df: pd.DataFrame) -> pd.DataFrame:
    return move_column('Fiyat', 0, df)

@register_command(r"tekrar eden satırları sil")
def cmd_drop_duplicates_command(match, df: pd.DataFrame) -> pd.DataFrame:
    return drop_duplicates(df)

@register_command(r"yalnızca 'toplam' olan satırları al")
def cmd_filter_total_command(match, df: pd.DataFrame) -> pd.DataFrame:
    return df[df.apply(lambda row: row.astype(str).str.contains('Toplam', case=False).any(), axis=1)]

def handle_command(text: str, df: pd.DataFrame) -> pd.DataFrame:
    for pattern, func in COMMAND_MAP.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return func(m, df)
    raise ValueError(f"No command matched: {text}")
