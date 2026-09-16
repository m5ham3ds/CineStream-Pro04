package com.example.utils

import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Environment
import android.widget.Toast

object AndroidDownloader {
    fun downloadVideo(context: Context, url: String, title: String, id: String) {
        try {
            val extension = ".mp4"
            val fileName = "${id}$extension"
            
            val destFile = java.io.File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "CineStream/$fileName")
            if (destFile.exists()) destFile.delete()

            if (url.contains(".m3u8")) {
                val intent = android.content.Intent(context, StreamDownloaderService::class.java).apply {
                    putExtra("url", url)
                    putExtra("title", title)
                    putExtra("id", id)
                }
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                    context.startForegroundService(intent)
                } else {
                    context.startService(intent)
                }
                Toast.makeText(context, "M3U8 Stream download started! Check notifications.", Toast.LENGTH_SHORT).show()
                return
            }
            
            val request = DownloadManager.Request(Uri.parse(url))
                .setTitle(title)
                .setDescription("Downloading Video via CinematicDownloader")
                .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                .setDestinationInExternalPublicDir(Environment.DIRECTORY_MOVIES, "CineStream/$fileName")
                .setAllowedOverMetered(true)
                .setAllowedOverRoaming(true)
                .addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
                .addRequestHeader("Referer", url)

            val downloadManager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
            downloadManager.enqueue(request)
            
            Toast.makeText(context, "Download started! Check notifications.", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(context, "Download failed: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }
}
