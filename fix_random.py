import re
with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("(0.02f .. 0.05f).random()", "0.03f")

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "w") as f:
    f.write(content)
