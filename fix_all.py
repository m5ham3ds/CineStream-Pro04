import re

# 1. AndroidDownloader as an object
with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "r") as f:
    c = f.read()

c = c.replace(
    'class AndroidDownloader(\n    private val context: Context\n) : Downloader {\n\n    override fun downloadFile(url: String, fileName: String, mediaId: String): Long {',
    'object AndroidDownloader {\n\n    fun downloadVideo(context: Context, url: String, fileName: String, mediaId: String): Long {'
)
c = c.replace('import com.example.domain.repository.Downloader', '')

with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "w") as f:
    f.write(c)

# 2. Revert PlayerScreen.kt
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    c = f.read()

c = c.replace(
    'com.example.utils.AndroidDownloader(context).downloadFile(url, "${uiState.title} - $quality.mp4", uiState.mediaId)',
    'com.example.utils.AndroidDownloader.downloadVideo(context, url, "${uiState.title} - $quality.mp4", uiState.mediaId)'
)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(c)

# 3. StreamDownloaderService
with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "r") as f:
    c = f.read()

c = c.replace('import kotlinx.coroutines.sync.withLock', 'import kotlinx.coroutines.sync.withPermit')
c = c.replace('semaphore.withLock {', 'semaphore.withPermit {')
c = c.replace('val mutex = Mutex()', '')

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "w") as f:
    f.write(c)

print("Fixed")
