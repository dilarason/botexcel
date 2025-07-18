import pandas as pd
import pytest
from modules.nlp_command_handler import handle_command

@pytest.fixture
def sample_df():
    return pd.DataFrame({'Ad':['Ali','Veli','Ali'], 'Fiyat':[10,20,10], 'Toplam':[100,200,100]})

def test_move_price_first(sample_df):
    df2 = handle_command("Fiyat sütununu ilk sıraya al", sample_df.copy())
    assert list(df2.columns)[0] == "Fiyat"

def test_drop_duplicates(sample_df):
    df2 = handle_command("tekrar eden satırları sil", sample_df.copy())
    assert df2.shape[0] == 2

def test_filter_total(sample_df):
    df2 = handle_command("yalnızca 'Toplam' olan satırları al", sample_df.copy())
    assert set(df2.index) == set(sample_df.index)
