with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "r") as f:
    c = f.read()

# Add a helper function to update DB
db_helper = """
    private fun updateDbProgress(fileId: String, progress: Float, isCompleted: Boolean = false) {
        serviceScope.launch {
            try {
                val db = com.example.data.db.AppDatabase.getDatabase(this@StreamDownloaderService)
                val dao = db.downloadDao()
                val item = dao.getDownloadByIdSync(fileId)
                if (item != null) {
                    val updated = item.copy(progress = progress, isCompleted = isCompleted)
                    dao.update(updated)
                }
            } catch (e: Exception) { e.printStackTrace() }
        }
    }
"""

c = c.replace("private fun getHeaders", db_helper + "\n    private fun getHeaders")

# Find updateNotification in downloadMp4 and downloadM3u8 and add updateDbProgress
c = c.replace(
    'updateNotification(title, "Downloading... ${(total * 100 / contentLength)}%", total.toInt(), contentLength.toInt(), true)',
    'updateNotification(title, "Downloading... ${(total * 100 / contentLength)}%", total.toInt(), contentLength.toInt(), true)\n                                            updateDbProgress(fileId, total.toFloat() / contentLength.toFloat())'
)

c = c.replace(
    'updateNotification(title, "Download complete", 0, 0, false)',
    'updateNotification(title, "Download complete", 0, 0, false)\n        updateDbProgress(fileId, 1.0f, true)'
)

c = c.replace(
    'val c = downloadedCount.incrementAndGet()\n                                updateNotification(title, "Downloading... $c / ${segments.size} parts", c, segments.size, true)',
    'val c = downloadedCount.incrementAndGet()\n                                updateNotification(title, "Downloading... $c / ${segments.size} parts", c, segments.size, true)\n                                updateDbProgress(fileId, c.toFloat() / segments.size.toFloat())'
)

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "w") as f:
    f.write(c)

