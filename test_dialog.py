import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Let's find where the Dialog starts and ends
start_idx = content.find("Dialog(\n")
if start_idx == -1:
    start_idx = content.find("Dialog(")

# Find the end of Dialog using brace matching
brace_count = 0
end_idx = -1
in_dialog = False

for i in range(start_idx, len(content)):
    if content[i] == '{':
        in_dialog = True
        brace_count += 1
    elif content[i] == '}':
        brace_count -= 1
        if in_dialog and brace_count == 0:
            end_idx = i
            break

print(f"Start: {start_idx}, End: {end_idx}")
