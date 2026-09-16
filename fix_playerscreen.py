import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    c = f.read()

c = c.replace(
    'com.example.utils.AndroidDownloader.downloadVideo(context, url, "${uiState.title} - $quality", fileId)',
    'com.example.utils.AndroidDownloader(context).downloadFile(url, "${uiState.title} - $quality.mp4", uiState.mediaId)'
)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(c)

