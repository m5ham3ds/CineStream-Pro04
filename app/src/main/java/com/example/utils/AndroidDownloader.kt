package com.example.utils

import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Environment
import android.widget.Toast

object AndroidDownloader {
    fun downloadVideo(context: Context, url: String, title: String) {
        try {
            // Clean title for file system
            val safeTitle = title.replace(Regex("[^a-zA-Z0-9.\\-]"), "_")
            
            // Check if it's HLS (.m3u8). Android DownloadManager natively supports standard files (.mp4, .mkv, .ts)
            // It will download .m3u8 as a tiny text file instead of the full video.
            // For a production streaming app, ExoPlayer DownloadService is used for m3u8, 
            // but we provide the standard system DownloadManager here for mp4 links.
            if (url.contains(".m3u8")) {
                Toast.makeText(context, "Downloading stream playlist (M3U8). Offline playback requires MP4.", Toast.LENGTH_LONG).show()
            }

            val extension = if (url.contains(".mp4")) ".mp4" else if (url.contains(".m3u8")) ".m3u8" else ".mp4"
            val fileName = "${safeTitle}_${System.currentTimeMillis()}$extension"

            val request = DownloadManager.Request(Uri.parse(url))
                .setTitle(title)
                .setDescription("Downloading Video via CinematicDownloader")
                .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                .setDestinationInExternalPublicDir(Environment.DIRECTORY_MOVIES, "CineStream/$fileName")
                .setAllowedOverMetered(true)
                .setAllowedOverRoaming(true)

            val downloadManager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
            downloadManager.enqueue(request)
            
            Toast.makeText(context, "Download started! Check notifications.", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(context, "Download failed: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }
}
