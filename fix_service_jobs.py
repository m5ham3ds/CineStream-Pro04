with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "r") as f:
    c = f.read()

c = c.replace(
    'class StreamDownloaderService : Service() {',
    'class StreamDownloaderService : Service() {\n    private val activeJobs = mutableMapOf<String, Job>()\n    private val activeNotifications = mutableMapOf<String, Int>()'
)

c = c.replace(
    'override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {',
    '''override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action
        if (action == "CANCEL") {
            val fileId = intent.getStringExtra("id") ?: return START_NOT_STICKY
            cancelDownload(fileId)
            return START_NOT_STICKY
        }
        if (action == "PAUSE") {
            // Not fully implemented, just cancel for now or update DB
            return START_NOT_STICKY
        }'''
)

c = c.replace(
    'val notificationId = fileId.hashCode()\n        startForeground(notificationId, notification)',
    'val notificationId = fileId.hashCode()\n        activeNotifications[fileId] = notificationId\n        startForeground(notificationId, notification)'
)

c = c.replace(
    'serviceScope.launch {',
    'val job = serviceScope.launch {'
)

c = c.replace(
    'val job = serviceScope.launch {',
    'val job = serviceScope.launch {'
)

# wait, I'll write a python script to cleanly rewrite the necessary parts
