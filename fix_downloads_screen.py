import re
with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "r") as f:
    c = f.read()

c = re.sub(r'// Simulate download progress\s*LaunchedEffect\(downloads\) \{.*?\n    \}\n', '', c, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "w") as f:
    f.write(c)

