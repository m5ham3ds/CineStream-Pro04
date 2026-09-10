package com.example.data.repository

import android.content.Context
import androidx.room.Room
import com.example.data.db.AppDatabase
import com.example.data.model.DownloadItem
import com.example.utils.NotificationHelper
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream

class DownloadRepository(private val context: Context) {
    private val db = AppDatabase.getDatabase(context)
    private val downloadDao = db.downloadDao()
    private val scope = CoroutineScope(Dispatchers.IO)
    private val client = OkHttpClient()

    fun getDownloadItems(): Flow<List<DownloadItem>> {
        return downloadDao.getAllItems()
    }

        suspend fun addCompletedDownload(item: DownloadItem) {
        downloadDao.insertItem(item)
    }

    suspend fun addToDownloads(item: DownloadItem) {
        downloadDao.insertItem(item)
        NotificationHelper.showDownloadStarted(context, item.title)
        
        // Start real download
        startRealDownload(item.id)
    }

    suspend fun updateDownload(item: DownloadItem) {
        downloadDao.updateItem(item)
    }

    suspend fun removeFromDownloads(item: DownloadItem) {
        downloadDao.deleteItem(item)
        // Also remove the file
        val file = File(context.filesDir, "downloads/${item.id}.mp4")
        if (file.exists()) {
            file.delete()
        }
    }

    private fun startRealDownload(id: String) {
        scope.launch {
            var currentItem = downloadDao.getItemById(id) ?: return@launch
            if (currentItem.isCompleted) return@launch

            // Use a sample real MP4 video to prove offline playback works
            val videoUrl = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
            
            val request = Request.Builder().url(videoUrl).build()
            
            try {
                val response = client.newCall(request).execute()
                if (!response.isSuccessful) throw Exception("Failed to download file")
                
                val body = response.body ?: throw Exception("Empty body")
                val contentLength = body.contentLength()
                
                val dir = File(context.filesDir, "downloads")
                if (!dir.exists()) dir.mkdirs()
                
                val file = File(dir, "${id}.mp4")
                val inputStream: InputStream = body.byteStream()
                val outputStream = FileOutputStream(file)
                
                val buffer = ByteArray(8 * 1024)
                var bytesRead: Int
                var totalBytesRead: Long = 0
                
                var lastUpdateTime = System.currentTimeMillis()

                inputStream.use { input ->
                    outputStream.use { output ->
                        while (input.read(buffer).also { bytesRead = it } != -1) {
                            // Check if paused or deleted
                            val checkItem = downloadDao.getItemById(id)
                            if (checkItem == null) {
                                // Deleted
                                file.delete()
                                return@launch
                            }
                            if (checkItem.isPaused) {
                                // For simplicity in this demo, if paused, we just delay and wait
                                // A real implementation would close streams and resume with Range headers
                                delay(1000)
                                continue
                            }

                            output.write(buffer, 0, bytesRead)
                            totalBytesRead += bytesRead
                            
                            val currentTime = System.currentTimeMillis()
                            if (currentTime - lastUpdateTime > 500) { // Update DB every 500ms max
                                val progress = if (contentLength > 0) totalBytesRead.toFloat() / contentLength.toFloat() else 0f
                                
                                currentItem = currentItem.copy(
                                    progress = progress.coerceAtMost(0.99f)
                                )
                                downloadDao.updateItem(currentItem)
                                lastUpdateTime = currentTime
                            }
                        }
                    }
                }
                
                // Done
                currentItem = downloadDao.getItemById(id) ?: return@launch
                currentItem = currentItem.copy(progress = 1f, isCompleted = true)
                downloadDao.updateItem(currentItem)
                NotificationHelper.showDownloadCompleted(context, currentItem.title)

            } catch (e: Exception) {
                e.printStackTrace()
                // Handle error by pausing
                currentItem = downloadDao.getItemById(id) ?: return@launch
                currentItem = currentItem.copy(isPaused = true)
                downloadDao.updateItem(currentItem)
            }
        }
    }
}
