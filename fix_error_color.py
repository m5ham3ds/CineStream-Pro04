import re

file_path = "app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt"
with open(file_path, "r") as f:
    content = f.read()

# Replace MaterialTheme.colorScheme.error with SuccessGreen
content = content.replace("MaterialTheme.colorScheme.errorContainer", "SuccessGreen.copy(alpha = 0.15f)")
content = content.replace("MaterialTheme.colorScheme.error", "SuccessGreen")

with open(file_path, "w") as f:
    f.write(content)

