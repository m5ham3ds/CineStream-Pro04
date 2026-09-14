with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    lines = f.readlines()

start_line = -1
for i, line in enumerate(lines):
    if "if (!isCloudflare) {" in line:
        start_line = i
        break

if start_line != -1:
    brace_count = 0
    in_block = False
    for i in range(start_line, len(lines)):
        if "{" in lines[i]:
            brace_count += lines[i].count("{")
            in_block = True
        if "}" in lines[i]:
            brace_count -= lines[i].count("}")
        if in_block and brace_count == 0:
            print(f"End line: {i+1}")
            break
