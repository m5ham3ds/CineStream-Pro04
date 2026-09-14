import re
with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Add context definition if missing
if "val context = LocalContext.current" not in content:
    content = re.sub(r'(fun ServerSelectionDialog.*?\{)', r'\1\n    val context = androidx.compose.ui.platform.LocalContext.current', content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
print("Fixed context in ServerSelectionDialog")
