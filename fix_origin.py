import re
with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "r") as f:
    content = f.read()

content = content.replace("playsinline=1\"", "playsinline=1&origin=https://www.youtube.com\"")

with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "w") as f:
    f.write(content)
