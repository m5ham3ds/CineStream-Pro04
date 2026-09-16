package com.example.utils

import android.app.NotificationChannel
import android.app.NotificationManager
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
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream
import java.io.RandomAccessFile
import java.net.URI
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger
import java.util.concurrent.atomic.AtomicLong
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withPermit
import kotlinx.coroutines.sync.Semaphore

class StreamDownloaderService : Service() {
    private val serviceJob = Job()
    private val serviceScope = CoroutineScope(Dispatchers.IO + serviceJob)
    private val CHANNEL_ID = "stream_download_channel"
    private val NOTIFICATION_ID = 10101
    
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
        val url = intent?.getStringExtra("url") ?: return START_NOT_STICKY
        val title = intent.getStringExtra("title") ?: "Video"
        val fileId = intent.getStringExtra("id") ?: System.currentTimeMillis().toString()
        
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Downloading $title")
            .setContentText("Initializing download...")
            .setSmallIcon(android.R.drawable.stat_sys_download)
            .setOngoing(true)
            .build()
            
        startForeground(NOTIFICATION_ID, notification)
        
        serviceScope.launch {
            try {
                val prefs = UserPreferencesRepository(this@StreamDownloaderService)
                val maxConcurrent = prefs.maxConcurrentDownloads.first()
                val maxSegments = prefs.maxSegments.first()
                
                if (url.contains(".m3u8")) {
                    downloadM3u8(url, title, fileId, maxConcurrent)
                } else {
                    downloadMp4(url, title, fileId, maxSegments)
                }
            } catch (e: Exception) {
                e.printStackTrace()
                updateNotification(title, "Download failed: ${e.message}", 0, 0, false)
            } finally {
                stopForeground(false)
                stopSelf()
            }
        }
        
        return START_NOT_STICKY
    }

    private fun updateNotification(title: String, text: String, progress: Int, max: Int, ongoing: Boolean) {
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
        notificationManager.notify(NOTIFICATION_ID, builder.build())
    }
    
    
    private fun updateDbProgress(fileId: String, progress: Float, isCompleted: Boolean = false) {
        serviceScope.launch {
            try {
                val db = com.example.data.db.AppDatabase.getDatabase(this@StreamDownloaderService)
                val dao = db.downloadDao()
                val item = dao.getItemById(fileId)
                if (item != null) {
                    val updated = item.copy(progress = progress, isCompleted = isCompleted)
                    dao.updateItem(updated)
                }
            } catch (e: Exception) { e.printStackTrace() }
        }
    }

    private fun getHeaders(url: String): Request.Builder {
        return Request.Builder()
            .url(url)
            .addHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
            .addHeader("Referer", url)
            .addHeader("Accept", "*/*")
    }

    private suspend fun downloadMp4(url: String, title: String, fileId: String, maxSegments: Int) {
        val dir = getExternalFilesDir(Environment.DIRECTORY_MOVIES) ?: File(filesDir, "movies")
        java.io.File(dir, ".nomedia").createNewFile()
        if (!dir.exists()) dir.mkdirs()
        val destFile = File(dir, "${fileId}.mp4")
        if (destFile.exists()) destFile.delete()

        // 1. Get file size
        val headReq = getHeaders(url).head().build()
        val response = client.newCall(headReq).execute()
        val contentLengthStr = response.header("Content-Length")
        val acceptRanges = response.header("Accept-Ranges")
        val contentLength = contentLengthStr?.toLongOrNull() ?: -1L
        
        if (contentLength > 0 && acceptRanges == "bytes" && maxSegments > 1) {
            // Multi-part download
            val partSize = contentLength / maxSegments
            val semaphore = Semaphore(maxSegments)
            val downloadedBytes = AtomicLong(0)
            
            val raf = RandomAccessFile(destFile, "rw")
            raf.setLength(contentLength)
            raf.close()
            
            val deferreds = (0 until maxSegments).map { i ->
                serviceScope.async(Dispatchers.IO) {
                    semaphore.withPermit {
                        val start = i * partSize
                        val end = if (i == maxSegments - 1) contentLength - 1 else (start + partSize - 1)
                        var success = false
                        var retries = 3
                        while (!success && retries > 0) {
                            try {
                                val req = getHeaders(url).header("Range", "bytes=$start-$end").build()
                                val res = client.newCall(req).execute()
                                if (res.isSuccessful) {
                                    val partRaf = RandomAccessFile(destFile, "rw")
                                    partRaf.seek(start)
                                    val stream = res.body?.byteStream()
                                    val buffer = ByteArray(8192)
                                    var read: Int
                                    while (stream?.read(buffer).also { read = it ?: -1 } != -1) {
                                        partRaf.write(buffer, 0, read)
                                        val total = downloadedBytes.addAndGet(read.toLong())
                                        if (total % (1024 * 512) == 0L) { // Update roughly every 500KB
                                            updateNotification(title, "Downloading... ${(total * 100 / contentLength)}%", total.toInt(), contentLength.toInt(), true)
                                            updateDbProgress(fileId, total.toFloat() / contentLength.toFloat())
                                        }
                                    }
                                    partRaf.close()
                                    res.close()
                                    success = true
                                }
                            } catch (e: Exception) {
                                retries--
                                if (retries == 0) throw e
                            }
                        }
                    }
                }
            }
            deferreds.awaitAll()
        } else {
            // Single-part download
            val req = getHeaders(url).build()
            val res = client.newCall(req).execute()
            if (!res.isSuccessful) throw Exception("Failed to download file")
            
            val stream = res.body?.byteStream()
            val output = FileOutputStream(destFile)
            val buffer = ByteArray(8192)
            var read: Int
            val downloadedBytes = AtomicLong(0)
            
            while (stream?.read(buffer).also { read = it ?: -1 } != -1) {
                output.write(buffer, 0, read)
                val total = downloadedBytes.addAndGet(read.toLong())
                if (contentLength > 0 && total % (1024 * 512) == 0L) {
                    updateNotification(title, "Downloading... ${(total * 100 / contentLength)}%", total.toInt(), contentLength.toInt(), true)
                                            updateDbProgress(fileId, total.toFloat() / contentLength.toFloat())
                } else if (contentLength <= 0 && total % (1024 * 1024) == 0L) {
                    updateNotification(title, "Downloading... ${total / (1024 * 1024)} MB", 0, 0, true)
                }
            }
            output.close()
            res.close()
        }
        
        updateNotification(title, "Download complete", 0, 0, false)
        updateDbProgress(fileId, 1.0f, true)
    }

    private suspend fun downloadM3u8(m3u8Url: String, title: String, fileId: String, maxConcurrent: Int) {
        val segments = mutableListOf<String>()
        var baseUrl = m3u8Url
        
        var req = getHeaders(m3u8Url).build()
        var res = client.newCall(req).execute()
        var content = res.body?.string() ?: throw Exception("Failed to fetch M3U8")
        
        if (content.contains("EXT-X-STREAM-INF")) {
            val lines = content.split("\n")
            for (line in lines) {
                if (line.isNotEmpty() && !line.startsWith("#")) {
                    baseUrl = URI(m3u8Url).resolve(line.trim()).toString()
                    req = getHeaders(baseUrl).build()
                    res = client.newCall(req).execute()
                    content = res.body?.string() ?: ""
                    break
                }
            }
        }
        
        val lines = content.split("\n")
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
        
        
        // Download segments to temp files concurrently
        val tempDir = File(dir, "temp_$fileId")
        if (!tempDir.exists()) tempDir.mkdirs()
        
        val deferreds = segments.mapIndexed { index, segmentUrl ->
            serviceScope.async(Dispatchers.IO) {
                semaphore.withPermit {
                    var success = false
                    var retries = 3
                    val tempFile = File(tempDir, "seg_$index.ts")
                    while (!success && retries > 0) {
                        try {
                            val sReq = getHeaders(segmentUrl).build()
                            val sRes = client.newCall(sReq).execute()
                            if (sRes.isSuccessful) {
                                val sStream = sRes.body?.byteStream()
                                val sOutput = FileOutputStream(tempFile)
                                val sBuffer = ByteArray(8192)
                                var sRead: Int
                                while (sStream?.read(sBuffer).also { sRead = it ?: -1 } != -1) {
                                    sOutput.write(sBuffer, 0, sRead)
                                }
                                sOutput.close()
                                sRes.close()
                                success = true
                                val c = downloadedCount.incrementAndGet()
                                updateNotification(title, "Downloading... $c / ${segments.size} parts", c, segments.size, true)
                                updateDbProgress(fileId, c.toFloat() / segments.size.toFloat())
                            } else {
                                retries--
                            }
                        } catch (e: Exception) {
                            retries--
                            if (retries == 0) throw e
                        }
                    }
                }
            }
        }
        deferreds.awaitAll()
        
        // Merge segments
        updateNotification(title, "Merging video...", segments.size, segments.size, true)
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

        updateNotification(title, "Download complete", 0, 0, false)
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
