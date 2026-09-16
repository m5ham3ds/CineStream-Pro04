with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    lines = f.readlines()

new_lines = []
seen = set()
for line in lines:
    if "<string name=\"confirm_sign_out\">" in line:
        if "confirm_sign_out" not in seen:
            seen.add("confirm_sign_out")
            new_lines.append(line)
    elif "<string name=\"help_support\">" in line:
        if "help_support" not in seen:
            seen.add("help_support")
            new_lines.append(line)
    else:
        new_lines.append(line)

with open("app/src/main/res/values-ar/strings.xml", "w") as f:
    f.writelines(new_lines)
