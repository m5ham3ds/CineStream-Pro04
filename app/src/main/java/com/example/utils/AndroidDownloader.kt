package com.example.utils

import android.content.Context
import android.widget.Toast


object AndroidDownloader {

    fun downloadVideo(context: Context, url: String, fileName: String, mediaId: String): Long {
        return try {
            val id = fileName.replace(".mp4", "").replace("CineStream/", "")
            val title = fileName.replace(".mp4", "")
            
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
            Toast.makeText(context, "Download started! Check notifications.", Toast.LENGTH_SHORT).show()
            System.currentTimeMillis() // return a fake long ID for DB compat
        } catch (e: Exception) {
            e.printStackTrace()
            0L
        }
    }
}
