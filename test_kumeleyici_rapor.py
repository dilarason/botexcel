# test_kumeleyici_rapor.py

from test_data import test_data
from kumeleyici_rapor import group_and_summary

summary = group_and_summary(test_data, group_key="Key")
print("Gruplama Sonucu:")
for row in summary:
    print(row)
