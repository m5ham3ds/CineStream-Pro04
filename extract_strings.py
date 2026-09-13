import os
import re

directories_to_scan = ['app/src/main/java/com/example/ui']

strings_found = set()

for root, dirs, files in os.walk(directories_to_scan[0]):
    for file in files:
        if file.endswith('.kt'):
            with open(os.path.join(root, file), 'r') as f:
                content = f.read()
            
            # Find Text("...")
            matches = re.findall(r'Text\(\s*"([^"]+)"', content)
            strings_found.update(matches)
            
            # Find Text(text = "...")
            matches2 = re.findall(r'Text\(\s*text\s*=\s*"([^"]+)"', content)
            strings_found.update(matches2)

# Also placeholders, labels, titles, etc. that might use string literals
# placeholder = { Text("...") } is already caught by the above regex!

with open("extracted_strings.txt", "w") as f:
    for s in sorted(list(strings_found)):
        f.write(s + "\n")

print("Done. Extracted", len(strings_found), "strings.")
