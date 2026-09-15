with open("app/src/main/java/com/example/data/repository/DownloadRepository.kt", "r") as f:
    content = f.read()

# Replace startRealDownload with just Notification
new_repo = """
package com.example.data.repository

import android.content.Context
import com.example.data.db.AppDatabase
import com.example.data.model.DownloadItem
import com.example.utils.NotificationHelper
import kotlinx.coroutines.flow.Flow
import java.io.File

class DownloadRepository(private val context: Context) {
    private val db = AppDatabase.getDatabase(context)
    private val downloadDao = db.downloadDao()

    fun getDownloadItems(): Flow<List<DownloadItem>> {
        return downloadDao.getAllItems()
    }
    
    suspend fun getAllItemsSync(): List<DownloadItem> {
        return downloadDao.getAllItemsSync()
    }
    
    suspend fun getItemByIdSync(id: String): DownloadItem? {
        return downloadDao.getItemById(id)
    }

    suspend fun addCompletedDownload(item: DownloadItem) {
        downloadDao.insertItem(item)
    }

    suspend fun addToDownloads(item: DownloadItem) {
        downloadDao.insertItem(item)
        NotificationHelper.showDownloadStarted(context, item.title)
    }

    suspend fun updateDownload(item: DownloadItem) {
        downloadDao.updateItem(item)
        if (item.isPaused) {
            DownloadManagerService.pauseDownload(item.id)
        }
    }

    suspend fun removeFromDownloads(item: DownloadItem) {
        downloadDao.deleteItem(item)
        DownloadManagerService.pauseDownload(item.id)
        val file = File(context.filesDir, "downloads/${item.id}.mp4")
        if (file.exists()) {
            file.delete()
        }
    }
}
"""

with open("app/src/main/java/com/example/data/repository/DownloadRepository.kt", "w") as f:
    f.write(new_repo.strip())
