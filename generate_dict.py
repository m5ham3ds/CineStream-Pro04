import re

with open("extracted_strings.txt", "r") as f:
    strings = f.read().splitlines()

# Filter out strings that have no letters (Arabic or English)
valid_strings = []
for s in strings:
    if re.search(r'[A-Za-z\u0600-\u06FF]', s):
        valid_strings.append(s)

print("Total valid strings:", len(valid_strings))

# Generate a starter dictionary
with open("starter_dict.py", "w") as f:
    f.write("translation_dict = {\n")
    for s in valid_strings:
        f.write(f'    r"""{s}""": ("name", "", ""),\n')
    f.write("}\n")
