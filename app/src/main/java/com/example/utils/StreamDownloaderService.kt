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
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL

class StreamDownloaderService : Service() {

    private val serviceJob = Job()
    private val serviceScope = CoroutineScope(Dispatchers.IO + serviceJob)
    private val CHANNEL_ID = "stream_download_channel"
    private val NOTIFICATION_ID = 10101

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
            .setContentText("Initializing...")
            .setSmallIcon(android.R.drawable.stat_sys_download)
            .setOngoing(true)
            .build()

        startForeground(NOTIFICATION_ID, notification)

        serviceScope.launch {
            try {
                downloadStream(url, title, fileId)
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

        if (max > 0) {
            builder.setProgress(max, progress, false)
        }

        notificationManager.notify(NOTIFICATION_ID, builder.build())
    }

    private suspend fun downloadStream(m3u8Url: String, title: String, fileId: String) {
        val segments = mutableListOf<String>()
        var baseUrl = m3u8Url

        // 1. Fetch playlist
        var conn = URL(m3u8Url).openConnection() as HttpURLConnection
        var content = conn.inputStream.bufferedReader().use { it.readText() }
        
        // If it's a master playlist, it shouldn't be here since getQualities resolves it.
        // But just in case, find the first sub-playlist
        if (content.contains("EXT-X-STREAM-INF")) {
            val lines = content.split("\n")
            for (line in lines) {
                if (line.isNotEmpty() && !line.startsWith("#")) {
                    baseUrl = URI(m3u8Url).resolve(line.trim()).toString()
                    conn = URL(baseUrl).openConnection() as HttpURLConnection
                    content = conn.inputStream.bufferedReader().use { it.readText() }
                    break
                }
            }
        }

        // 2. Parse TS segments
        val lines = content.split("\n")
        for (line in lines) {
            if (line.isNotEmpty() && !line.startsWith("#")) {
                segments.add(URI(baseUrl).resolve(line.trim()).toString())
            }
        }

        if (segments.isEmpty()) {
            throw Exception("No video segments found")
        }

        // 3. Download segments
        val dir = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "CineStream")
        if (!dir.exists()) dir.mkdirs()
        
        val destFile = File(dir, "${fileId}.mp4")
        if (destFile.exists()) destFile.delete()

        FileOutputStream(destFile, true).use { output ->
            for ((index, segmentUrl) in segments.withIndex()) {
                updateNotification("Downloading $title", "Segment ${index + 1} of ${segments.size}", index, segments.size, true)
                
                var retries = 3
                var success = false
                while (retries > 0 && !success) {
                    try {
                        val segConn = URL(segmentUrl).openConnection() as HttpURLConnection
                        segConn.connectTimeout = 10000
                        segConn.readTimeout = 15000
                        segConn.inputStream.use { input ->
                            val buffer = ByteArray(8192)
                            var bytesRead: Int
                            while (input.read(buffer).also { bytesRead = it } != -1) {
                                output.write(buffer, 0, bytesRead)
                            }
                        }
                        success = true
                    } catch (e: Exception) {
                        retries--
                        if (retries == 0) throw Exception("Failed to download segment: $segmentUrl")
                        kotlinx.coroutines.delay(1000)
                    }
                }
            }
        }

        updateNotification(title, "Download complete", 0, 0, false)
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
