import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    c = f.read()

target = """                videoUrl?.let { url ->
                    com.example.utils.AndroidDownloader.downloadVideo(context, url, fileId, uiState.title)"""

replace = """                videoUrl?.let { url ->
                    com.example.utils.AndroidDownloader.downloadVideo(context, url, fileId, "${uiState.title} - $quality")"""

c = c.replace(target, replace)

# also change downloadItem title just in case it doesn't include it. Wait, the user sees downloadItem.title in DownloadsScreen
# Let's check how DownloadsScreen shows it. It shows item.title and item.quality separated.
# But for AndroidDownloader, the notification uses `title` parameter. So "${uiState.title} - $quality" is perfect for notification.

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(c)

