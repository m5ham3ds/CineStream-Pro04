import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

content = content.replace('videoUrl.startsWith("local_offline_file")', 'videoUrl.startsWith("file://")')

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
