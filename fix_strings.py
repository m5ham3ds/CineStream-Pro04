def fix_strings(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
    
    seen = set()
    new_lines = []
    for line in lines:
        if "<string name=\"cancel\">" in line:
            if "cancel" in seen:
                continue
            seen.add("cancel")
        new_lines.append(line)
        
    with open(filepath, "w") as f:
        f.writelines(new_lines)

fix_strings("app/src/main/res/values/strings.xml")
fix_strings("app/src/main/res/values-ar/strings.xml")
