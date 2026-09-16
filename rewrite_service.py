import re

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "r") as f:
    content = f.read()

# Add imports if missing
imports_to_add = """
import android.app.PendingIntent
import java.util.concurrent.ConcurrentHashMap
"""
content = content.replace('import java.net.URI', imports_to_add + '\nimport java.net.URI')

# Add maps
maps = """
    private val activeJobs = ConcurrentHashMap<String, Job>()
    private val activeNotifications = ConcurrentHashMap<String, Int>()
"""
content = content.replace('private val NOTIFICATION_ID = 10101', maps)

# update notification builder
builder_replace = """
    private fun updateNotification(notificationId: Int, title: String, text: String, progress: Int, max: Int, ongoing: Boolean, fileId: String = "") {
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val builder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(title)
            .setContentText(text)
            .setSmallIcon(if (ongoing) android.R.drawable.stat_sys_download else android.R.drawable.stat_sys_download_done)
            .setOngoing(ongoing)
            .setOnlyAlertOnce(true)

        if (max > 0) {
            builder.setProgress(max, progress, false)
        }
        
        if (ongoing && fileId.isNotEmpty()) {
            val cancelIntent = Intent(this, StreamDownloaderService::class.java).apply {
                action = "CANCEL"
                putExtra("id", fileId)
            }
            val cancelPendingIntent = PendingIntent.getService(this, notificationId, cancelIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            builder.addAction(android.R.drawable.ic_menu_close_clear_cancel, "Cancel", cancelPendingIntent)
        }
        
        notificationManager.notify(notificationId, builder.build())
    }
"""
content = re.sub(r'private fun updateNotification\(notificationId: Int, title: String, text: String, progress: Int, max: Int, ongoing: Boolean\) \{.*?\n    \}', builder_replace, content, flags=re.DOTALL)

# update onStartCommand
onstart = """
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action
        val fileId = intent?.getStringExtra("id") ?: return START_NOT_STICKY
        
        if (action == "CANCEL") {
            val job = activeJobs[fileId]
            job?.cancel()
            activeJobs.remove(fileId)
            
            val notifId = activeNotifications[fileId]
            if (notifId != null) {
                val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
                notificationManager.cancel(notifId)
                activeNotifications.remove(fileId)
            }
            
            // Delete files and db entry
            serviceScope.launch {
                try {
                    val db = com.example.data.db.AppDatabase.getDatabase(this@StreamDownloaderService)
                    val dao = db.downloadDao()
                    val item = dao.getItemById(fileId)
                    if (item != null) dao.deleteItem(item)
                    
                    val dir = getExternalFilesDir(Environment.DIRECTORY_MOVIES) ?: File(filesDir, "movies")
                    val destFile = File(dir, "${fileId}.mp4")
                    if (destFile.exists()) destFile.delete()
                    val tempDir = File(dir, "temp_$fileId")
                    if (tempDir.exists()) tempDir.deleteRecursively()
                } catch (e: Exception) {}
            }
            return START_NOT_STICKY
        }
        
        val title = intent.getStringExtra("title") ?: "Video"
        
        val notificationId = fileId.hashCode()
        activeNotifications[fileId] = notificationId
        
        val cancelIntent = Intent(this, StreamDownloaderService::class.java).apply {
            this.action = "CANCEL"
            putExtra("id", fileId)
        }
        val cancelPendingIntent = PendingIntent.getService(this, notificationId, cancelIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
        
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Downloading $title")
            .setContentText("Initializing download...")
            .setSmallIcon(android.R.drawable.stat_sys_download)
            .setOngoing(true)
            .addAction(android.R.drawable.ic_menu_close_clear_cancel, "Cancel", cancelPendingIntent)
            .build()
            
        startForeground(notificationId, notification)
        
        val job = serviceScope.launch {
            try {
                val prefs = UserPreferencesRepository(this@StreamDownloaderService)
                val maxConcurrent = prefs.maxConcurrentDownloads.first()
                val maxSegments = prefs.maxSegments.first()
                
                if (url.contains(".m3u8")) {
                    downloadM3u8(notificationId, url, title, fileId, maxConcurrent)
                } else {
                    downloadMp4(notificationId, url, title, fileId, maxSegments)
                }
            } catch (e: Exception) {
                if (e !is kotlinx.coroutines.CancellationException) {
                    e.printStackTrace()
                    updateNotification(notificationId, title, "Download failed: ${e.message}", 0, 0, false)
                }
            } finally {
                activeJobs.remove(fileId)
                if (activeJobs.isEmpty()) {
                    stopForeground(false)
                    stopSelf()
                }
            }
        }
        activeJobs[fileId] = job
        
        return START_NOT_STICKY
    }
"""
content = re.sub(r'override fun onStartCommand.*?return START_NOT_STICKY\n    \}', onstart, content, flags=re.DOTALL)

# update calls to updateNotification to include fileId
content = content.replace(
    'updateNotification(notificationId, title, "Downloading... ${(total * 100 / contentLength)}%", total.toInt(), contentLength.toInt(), true)',
    'updateNotification(notificationId, title, "Downloading... ${(total * 100 / contentLength)}%", total.toInt(), contentLength.toInt(), true, fileId)'
)
content = content.replace(
    'updateNotification(notificationId, title, "Downloading... ${total / (1024 * 1024)} MB", 0, 0, true)',
    'updateNotification(notificationId, title, "Downloading... ${total / (1024 * 1024)} MB", 0, 0, true, fileId)'
)
content = content.replace(
    'updateNotification(notificationId, title, "Downloading... $c / ${segments.size} parts", c, segments.size, true)',
    'updateNotification(notificationId, title, "Downloading... $c / ${segments.size} parts", c, segments.size, true, fileId)'
)
content = content.replace(
    'updateNotification(notificationId, title, "Merging video...", segments.size, segments.size, true)',
    'updateNotification(notificationId, title, "Merging video...", segments.size, segments.size, true, fileId)'
)

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "w") as f:
    f.write(content)

