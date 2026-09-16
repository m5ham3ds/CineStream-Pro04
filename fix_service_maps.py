with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "r") as f:
    c = f.read()

maps = """
    private val activeJobs = ConcurrentHashMap<String, Job>()
    private val activeNotifications = ConcurrentHashMap<String, Int>()
"""
c = c.replace(
    'private val CHANNEL_ID = "stream_download_channel"',
    'private val CHANNEL_ID = "stream_download_channel"' + maps
)

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "w") as f:
    f.write(c)

