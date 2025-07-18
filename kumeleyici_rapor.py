# kumeleyici_rapor.py

from collections import Counter

def group_and_summary(data, group_key="Key"):
    counter = Counter(row.get(group_key, "") for row in data if row.get(group_key))
    summary = [{"Group": k, "Count": v} for k, v in counter.items()]
    return summary

def add_summary_sheet(wb, summary_data, sheet_name="Summary"):
    ws = wb.create_sheet(title=sheet_name)
    ws.append(["Group", "Count"])
    for row in summary_data:
        ws.append([row["Group"], row["Count"]])

if __name__ == "__main__":
    from test_data import test_data
    summary = group_and_summary(test_data, group_key="Key")
    for row in summary:
        print(row)
