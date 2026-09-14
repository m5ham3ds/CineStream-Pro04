with open("temp_app_nav.kt", "r") as f:
    lines = f.readlines()

# Find the last `}` that closes the AppNavigation function.
# It should be the second to last line or last line.
for i in range(len(lines)-1, -1, -1):
    if lines[i].strip() == "}":
        lines.insert(i, "    }\n")
        break

with open("temp_app_nav.kt", "w") as f:
    f.writelines(lines)
