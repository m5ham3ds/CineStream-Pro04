import re

def remove_duplicates(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    seen = set()
    new_lines = []
    
    for line in lines:
        match = re.search(r'<string name="(.*?)">', line)
        if match:
            name = match.group(1)
            if name in seen:
                continue
            seen.add(name)
        new_lines.append(line)
        
    with open(filepath, "w") as f:
        f.writelines(new_lines)

remove_duplicates("app/src/main/res/values/strings.xml")
remove_duplicates("app/src/main/res/values-ar/strings.xml")

