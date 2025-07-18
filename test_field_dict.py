from field_dictionary import load_field_dict, update_field_dict_for_keys

data = [
    {"Key": "Adı", "Value": "Ahmet"},
    {"Key": "BARCODE", "Value": "12345"}
]

key_list = [row["Key"] for row in data]
field_dict = load_field_dict()
field_dict = update_field_dict_for_keys(key_list, field_dict)

for row in data:
    row["Type"] = field_dict[row["Key"]]["Type"]

print(data)
