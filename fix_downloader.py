import re

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "r") as f:
    c = f.read()

# 1. OkHttpClient Dispatcher and Connection Limit
target_client = """    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()"""
replace_client = """    private val dispatcher = okhttp3.Dispatcher().apply {
        maxRequests = 128
        maxRequestsPerHost = 64
    }
    private val client = OkHttpClient.Builder()
        .dispatcher(dispatcher)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()"""
c = c.replace(target_client, replace_client)

# 2. Add properties
target_props = """    private val pausedFlags = ConcurrentHashMap<String, Boolean>()"""
replace_props = """    private val pausedFlags = ConcurrentHashMap<String, Boolean>()
    private var runningDownloads = AtomicInteger(0)
    private var currentForegroundId: Int? = null

    private fun isWifiConnected(): Boolean {
        val connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
        return capabilities.hasTransport(android.net.NetworkCapabilities.TRANSPORT_WIFI)
    }"""
c = c.replace(target_props, replace_props)

# 3. Notification Logic
target_notif = """        if (ongoing) {
            startForeground(notificationId, builder.build())
        } else {
            notificationManager.notify(notificationId, builder.build())
        }"""
replace_notif = """        val notif = builder.build()
        if (ongoing) {
            if (currentForegroundId == null || currentForegroundId == notificationId) {
                currentForegroundId = notificationId
                startForeground(notificationId, notif)
            } else {
                notificationManager.notify(notificationId, notif)
            }
        } else {
            notificationManager.notify(notificationId, notif)
            if (currentForegroundId == notificationId) {
                val another = activeNotifications.values.firstOrNull { it != notificationId }
                if (another != null) {
                    currentForegroundId = another
                } else {
                    currentForegroundId = null
                }
            }
        }"""
c = c.replace(target_notif, replace_notif)

# 4. onStartCommand queueing and WiFi check
target_launch = """        val job = serviceScope.launch {
            try {
                val prefs = UserPreferencesRepository(this@StreamDownloaderService)
                val maxConcurrent = prefs.maxConcurrentDownloads.first()
                val maxSegments = prefs.maxSegments.first()
                
                if (url.contains(".m3u8")) {
                    downloadM3u8(notificationId, url, title, fileId, maxConcurrent)
                } else {
                    downloadMp4(notificationId, url, title, fileId, maxSegments)
                }
            } catch (e: Exception) {"""

replace_launch = """        val job = serviceScope.launch {
            try {
                val prefs = UserPreferencesRepository(this@StreamDownloaderService)
                val maxConcurrentMovies = prefs.maxConcurrentDownloads.first()
                val maxSegments = prefs.maxSegments.first()
                val networkType = prefs.downloadNetwork.first()
                
                if (networkType == 1) {
                    while (!isWifiConnected() && isActive) {
                        updateNotification(notificationId, title, "Waiting for WiFi...", 0, 0, true, fileId, false)
                        delay(5000)
                    }
                }
                
                while (runningDownloads.get() >= maxConcurrentMovies && isActive) {
                    updateNotification(notificationId, title, "Queued...", 0, 0, true, fileId, false)
                    delay(3000)
                }
                
                runningDownloads.incrementAndGet()
                
                if (url.contains(".m3u8")) {
                    downloadM3u8(notificationId, url, title, fileId, maxSegments)
                } else {
                    downloadMp4(notificationId, url, title, fileId, maxSegments)
                }
            } catch (e: Exception) {"""
c = c.replace(target_launch, replace_launch)

target_finally = """            } finally {
                activeJobs.remove(fileId)
                if (activeJobs.isEmpty()) {
                    stopForeground(false)
                    stopSelf()
                }
            }"""

replace_finally = """            } finally {
                runningDownloads.decrementAndGet()
                activeJobs.remove(fileId)
                if (activeJobs.isEmpty()) {
                    stopForeground(false)
                    stopSelf()
                }
            }"""
c = c.replace(target_finally, replace_finally)

# 5. Fix M3U8 progress display
target_m3u8_prog = """                                updateNotification(notificationId, title, "Downloading... $c / ${segments.size} parts", c, segments.size, true, fileId, false)"""
replace_m3u8_prog = """                                val percentage = (c * 100) / segments.size
                                updateNotification(notificationId, title, "Downloading... $percentage%", c, segments.size, true, fileId, false)"""
c = c.replace(target_m3u8_prog, replace_m3u8_prog)

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "w") as f:
    f.write(c)

