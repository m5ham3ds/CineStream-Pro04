with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "r") as f:
    c = f.read()

# Replace hardcoded NOTIFICATION_ID
c = c.replace('private val NOTIFICATION_ID = 10101\n', '')

# add notificationId to onStartCommand and download functions
# wait, updateNotification needs notificationId

c = c.replace(
    'private fun updateNotification(title: String, text: String, progress: Int, max: Int, ongoing: Boolean) {',
    'private fun updateNotification(notificationId: Int, title: String, text: String, progress: Int, max: Int, ongoing: Boolean) {'
)
c = c.replace('notificationManager.notify(NOTIFICATION_ID, builder.build())', 'notificationManager.notify(notificationId, builder.build())')

c = c.replace(
    'startForeground(NOTIFICATION_ID, notification)',
    'val notificationId = fileId.hashCode()\n        startForeground(notificationId, notification)'
)

c = c.replace(
    'downloadM3u8(url, title, fileId, maxConcurrent)',
    'downloadM3u8(notificationId, url, title, fileId, maxConcurrent)'
)
c = c.replace(
    'downloadMp4(url, title, fileId, maxSegments)',
    'downloadMp4(notificationId, url, title, fileId, maxSegments)'
)
c = c.replace(
    'updateNotification(title, "Download failed: ${e.message}", 0, 0, false)',
    'updateNotification(fileId.hashCode(), title, "Download failed: ${e.message}", 0, 0, false)'
)

c = c.replace(
    'private suspend fun downloadMp4(url: String, title: String, fileId: String, maxSegments: Int) {',
    'private suspend fun downloadMp4(notificationId: Int, url: String, title: String, fileId: String, maxSegments: Int) {'
)
c = c.replace(
    'private suspend fun downloadM3u8(m3u8Url: String, title: String, fileId: String, maxConcurrent: Int) {',
    'private suspend fun downloadM3u8(notificationId: Int, m3u8Url: String, title: String, fileId: String, maxConcurrent: Int) {'
)

c = c.replace('updateNotification(title', 'updateNotification(notificationId, title')

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "w") as f:
    f.write(c)

