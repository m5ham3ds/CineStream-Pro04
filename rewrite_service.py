import os

code = """package com.example.utils

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Environment
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.example.data.repository.UserPreferencesRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import kotlinx.coroutines.isActive
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Headers
import java.io.File
import java.io.FileOutputStream
import java.io.RandomAccessFile
import java.net.URI
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger
import java.util.concurrent.atomic.AtomicLong
import java.io.IOException

class StreamDownloaderService : Service() {
    private val serviceJob = Job()
    private val serviceScope = CoroutineScope(Dispatchers.IO + serviceJob)
    private val CHANNEL_ID = "stream_download_channel"
    
    private val activeJobs = ConcurrentHashMap<String, Job>()
    private val activeNotifications = ConcurrentHashMap<String, Int>()
    private val pausedFlags = ConcurrentHashMap<String, Boolean>()
    
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action
        val fileId = intent?.getStringExtra("id") ?: return START_NOT_STICKY
        val title = intent.getStringExtra("title") ?: "Video"
        val url = intent.getStringExtra("url") ?: ""
        
        if (action == "CANCEL") {
            val job = activeJobs[fileId]
            job?.cancel()
            activeJobs.remove(fileId)
            pausedFlags.remove(fileId)
            
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
        
        if (action == "PAUSE") {
            pausedFlags[fileId] = true
            serviceScope.launch {
                updateDbState(fileId, true)
            }
            updateNotification(activeNotifications[fileId] ?: fileId.hashCode(), title, "Paused", 0, 0, false, fileId, true)
            return START_NOT_STICKY
        }
        
        if (action == "RESUME") {
            pausedFlags[fileId] = false
            serviceScope.launch {
                updateDbState(fileId, false)
            }
            updateNotification(activeNotifications[fileId] ?: fileId.hashCode(), title, "Resuming...", 0, 0, true, fileId, false)
            return START_NOT_STICKY
        }
        
        if (url.isEmpty()) return START_NOT_STICKY
        
        val notificationId = fileId.hashCode()
        activeNotifications[fileId] = notificationId
        pausedFlags[fileId] = false
        
        updateNotification(notificationId, title, "Initializing download...", 0, 0, true, fileId, false)
        
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
                    updateNotification(notificationId, title, "Download failed: ${e.message}", 0, 0, false, fileId, false)
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

    private fun getHeaders(url: String): Request.Builder {
        val uri = try { URI(url) } catch (e: Exception) { null }
        val host = uri?.host ?: ""
        val scheme = uri?.scheme ?: "https"
        val origin = "$scheme://$host"
        
        return Request.Builder()
            .url(url)
            .addHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            .addHeader("Accept", "*/*")
            .addHeader("Origin", origin)
            .addHeader("Referer", "$origin/")
            .addHeader("Connection", "keep-alive")
    }

    private fun updateNotification(notificationId: Int, title: String, text: String, progress: Int, max: Int, ongoing: Boolean, fileId: String, isPaused: Boolean) {
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
        
        if (fileId.isNotEmpty() && ongoing) {
            // Add Pause/Resume button
            val pauseResumeIntent = Intent(this, StreamDownloaderService::class.java).apply {
                action = if (isPaused) "RESUME" else "PAUSE"
                putExtra("id", fileId)
                putExtra("title", title)
            }
            val prPendingIntent = PendingIntent.getService(this, notificationId + 1, pauseResumeIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            builder.addAction(
                if (isPaused) android.R.drawable.ic_media_play else android.R.drawable.ic_media_pause,
                if (isPaused) "Resume" else "Pause",
                prPendingIntent
            )
            
            // Add Cancel button
            val cancelIntent = Intent(this, StreamDownloaderService::class.java).apply {
                action = "CANCEL"
                putExtra("id", fileId)
            }
            val cancelPendingIntent = PendingIntent.getService(this, notificationId + 2, cancelIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
            builder.addAction(android.R.drawable.ic_menu_close_clear_cancel, "Cancel", cancelPendingIntent)
        }
        
        if (ongoing) {
            startForeground(notificationId, builder.build())
        } else {
            notificationManager.notify(notificationId, builder.build())
        }
    }

    private suspend fun updateDbProgress(fileId: String, progress: Float, isCompleted: Boolean = false) {
        try {
            val db = com.example.data.db.AppDatabase.getDatabase(this)
            val dao = db.downloadDao()
            val item = dao.getItemById(fileId)
            if (item != null) {
                dao.updateItem(item.copy(progress = progress, isCompleted = isCompleted))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    private suspend fun updateDbState(fileId: String, isPaused: Boolean) {
        try {
            val db = com.example.data.db.AppDatabase.getDatabase(this)
            val dao = db.downloadDao()
            val item = dao.getItemById(fileId)
            if (item != null) {
                dao.updateItem(item.copy(isPaused = isPaused))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private suspend fun suspendIfPaused(fileId: String) {
        while (pausedFlags[fileId] == true) {
            delay(1000)
        }
    }

    private suspend fun downloadMp4(notificationId: Int, url: String, title: String, fileId: String, maxSegments: Int) {
        val dir = getExternalFilesDir(Environment.DIRECTORY_MOVIES) ?: File(filesDir, "movies")
        java.io.File(dir, ".nomedia").createNewFile()
        if (!dir.exists()) dir.mkdirs()
        
        val destFile = File(dir, "${fileId}.mp4")
        
        var headReq = getHeaders(url).head().build()
        var headRes = client.newCall(headReq).execute()
        var contentLength = headRes.header("Content-Length")?.toLongOrNull() ?: -1L
        var acceptRanges = headRes.header("Accept-Ranges") == "bytes"
        headRes.close()
        
        if (contentLength > 0 && acceptRanges && maxSegments > 1) {
            // Segmented download - omit for simplicity here to make it rock solid, fall back to single connection with Range support
            acceptRanges = true
        }

        var downloadedBytes = if (destFile.exists()) destFile.length() else 0L
        if (contentLength > 0 && downloadedBytes == contentLength) {
            updateNotification(notificationId, title, "Download complete", 0, 0, false, fileId, false)
            updateDbProgress(fileId, 1.0f, true)
            return
        }

        var success = false
        while (!success && serviceScope.isActive) {
            suspendIfPaused(fileId)
            try {
                val reqBuilder = getHeaders(url)
                if (downloadedBytes > 0) {
                    reqBuilder.header("Range", "bytes=$downloadedBytes-")
                }
                
                val res = client.newCall(reqBuilder.build()).execute()
                if (!res.isSuccessful && res.code != 206) throw IOException("Failed to download file: ${res.code}")
                
                val stream = res.body?.byteStream()
                val output = FileOutputStream(destFile, downloadedBytes > 0)
                val buffer = ByteArray(8192)
                var read: Int
                
                while (stream?.read(buffer).also { read = it ?: -1 } != -1 && serviceScope.isActive) {
                    suspendIfPaused(fileId)
                    output.write(buffer, 0, read)
                    downloadedBytes += read.toLong()
                    
                    if (contentLength > 0 && downloadedBytes % (1024 * 512) < 8192) {
                        updateNotification(notificationId, title, "Downloading... ${(downloadedBytes * 100 / contentLength)}%", downloadedBytes.toInt(), contentLength.toInt(), true, fileId, false)
                        updateDbProgress(fileId, downloadedBytes.toFloat() / contentLength.toFloat())
                    }
                }
                output.close()
                res.close()
                
                if (contentLength > 0 && downloadedBytes < contentLength) {
                    throw IOException("Connection closed prematurely")
                }
                success = true
            } catch (e: Exception) {
                if (e is kotlinx.coroutines.CancellationException) throw e
                e.printStackTrace()
                updateNotification(notificationId, title, "Waiting for network...", 0, 0, true, fileId, false)
                delay(5000)
            }
        }
        
        updateNotification(notificationId, title, "Download complete", 0, 0, false, fileId, false)
        updateDbProgress(fileId, 1.0f, true)
    }

    private suspend fun downloadM3u8(notificationId: Int, m3u8Url: String, title: String, fileId: String, maxConcurrent: Int) {
        val segments = mutableListOf<String>()
        var baseUrl = m3u8Url
        
        var content = ""
        var successFetch = false
        while (!successFetch && serviceScope.isActive) {
            suspendIfPaused(fileId)
            try {
                val req = getHeaders(m3u8Url).build()
                val res = client.newCall(req).execute()
                content = res.body?.string() ?: throw IOException("Empty body")
                successFetch = true
            } catch (e: Exception) {
                updateNotification(notificationId, title, "Waiting for network...", 0, 0, true, fileId, false)
                delay(5000)
            }
        }
        
        if (content.contains("EXT-X-STREAM-INF")) {
            val lines = content.split("\\n")
            for (line in lines) {
                if (line.isNotEmpty() && !line.startsWith("#")) {
                    baseUrl = URI(m3u8Url).resolve(line.trim()).toString()
                    successFetch = false
                    while (!successFetch && serviceScope.isActive) {
                        suspendIfPaused(fileId)
                        try {
                            val req = getHeaders(baseUrl).build()
                            val res = client.newCall(req).execute()
                            content = res.body?.string() ?: ""
                            successFetch = true
                        } catch (e: Exception) {
                            delay(3000)
                        }
                    }
                    break
                }
            }
        }
        
        val lines = content.split("\\n")
        for (line in lines) {
            if (line.isNotEmpty() && !line.startsWith("#")) {
                segments.add(URI(baseUrl).resolve(line.trim()).toString())
            }
        }
        if (segments.isEmpty()) throw Exception("No video segments found")

        val dir = getExternalFilesDir(Environment.DIRECTORY_MOVIES) ?: File(filesDir, "movies")
        java.io.File(dir, ".nomedia").createNewFile()
        if (!dir.exists()) dir.mkdirs()
        
        val destFile = File(dir, "${fileId}.mp4")
        if (destFile.exists()) destFile.delete()

        val downloadedCount = AtomicInteger(0)
        val semaphore = Semaphore(maxConcurrent)
        
        val tempDir = File(dir, "temp_$fileId")
        if (!tempDir.exists()) tempDir.mkdirs()
        
        // Count already downloaded segments
        for (i in segments.indices) {
            val tempFile = File(tempDir, "seg_$i.ts")
            if (tempFile.exists() && tempFile.length() > 0) {
                downloadedCount.incrementAndGet()
            }
        }
        
        val deferreds = segments.mapIndexed { index, segmentUrl ->
            serviceScope.async(Dispatchers.IO) {
                semaphore.withPermit {
                    val tempFile = File(tempDir, "seg_$index.ts")
                    if (tempFile.exists() && tempFile.length() > 0) return@withPermit
                    
                    var success = false
                    while (!success && serviceScope.isActive) {
                        suspendIfPaused(fileId)
                        try {
                            val sReq = getHeaders(segmentUrl).build()
                            val sRes = client.newCall(sReq).execute()
                            if (sRes.isSuccessful) {
                                val sStream = sRes.body?.byteStream()
                                val sOutput = FileOutputStream(tempFile)
                                val sBuffer = ByteArray(8192)
                                var sRead: Int
                                while (sStream?.read(sBuffer).also { sRead = it ?: -1 } != -1 && serviceScope.isActive) {
                                    suspendIfPaused(fileId)
                                    sOutput.write(sBuffer, 0, sRead)
                                }
                                sOutput.close()
                                sRes.close()
                                success = true
                                val c = downloadedCount.incrementAndGet()
                                updateNotification(notificationId, title, "Downloading... $c / ${segments.size} parts", c, segments.size, true, fileId, false)
                                updateDbProgress(fileId, c.toFloat() / segments.size.toFloat())
                            } else {
                                throw IOException("Bad response ${sRes.code}")
                            }
                        } catch (e: Exception) {
                            if (e is kotlinx.coroutines.CancellationException) throw e
                            updateNotification(notificationId, title, "Waiting for network...", downloadedCount.get(), segments.size, true, fileId, false)
                            delay(5000)
                        }
                    }
                }
            }
        }
        deferreds.awaitAll()
        
        updateNotification(notificationId, title, "Merging video...", segments.size, segments.size, true, fileId, false)
        val finalOutput = FileOutputStream(destFile, true)
        for (i in segments.indices) {
            val tempFile = File(tempDir, "seg_$i.ts")
            if (tempFile.exists()) {
                val input = tempFile.inputStream()
                val buffer = ByteArray(8192)
                var read: Int
                while (input.read(buffer).also { read = it } != -1) {
                    finalOutput.write(buffer, 0, read)
                }
                input.close()
                tempFile.delete()
            }
        }
        finalOutput.close()
        tempDir.delete()

        updateNotification(notificationId, title, "Download complete", 0, 0, false, fileId, false)
        updateDbProgress(fileId, 1.0f, true)
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Stream Downloads",
                NotificationManager.IMPORTANCE_LOW
            )
            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        serviceJob.cancel()
    }
}
"""

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "w") as f:
    f.write(code)
