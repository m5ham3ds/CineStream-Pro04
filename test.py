import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

# Let's find extractingEmbedUrl?.let
idx = c.find("extractingEmbedUrl?.let { url ->")
print(f"Index: {idx}")
print(c[idx-500:idx])
