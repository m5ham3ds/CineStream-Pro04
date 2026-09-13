file_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(file_path, "r") as f:
    content = f.read()

# We need to remove the extra closing brace at the end of the file.
content = content.rstrip()
if content.endswith('}'):
    content = content[:-1]

with open(file_path, "w") as f:
    f.write(content)
