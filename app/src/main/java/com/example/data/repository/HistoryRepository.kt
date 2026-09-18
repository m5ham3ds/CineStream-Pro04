package com.example.data.repository

import android.content.Context
import com.example.data.db.AppDatabase
import com.example.data.model.HistoryItem
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.combine

class HistoryRepository(context: Context) {
    private val db = AppDatabase.getDatabase(context)
    private val historyDao = db.historyDao()
    private val downloadDao = db.downloadDao()
    private val auth = FirebaseAuth.getInstance()
    private val firestore = FirebaseFirestore.getInstance()

    fun getHistoryItems(): Flow<List<HistoryItem>> {
        return combine(historyDao.getAllHistory(), downloadDao.getAllItems()) { history, downloads ->
            val result = mutableListOf<HistoryItem>()
            result.addAll(history)
            
            // Include completed downloads even if they haven't been watched online yet
            val completedDownloads = downloads.filter { it.isCompleted }
            for (dl in completedDownloads) {
                val mediaId = dl.mediaId.ifEmpty { dl.id }
                val alreadyExists = result.any { it.id == mediaId || it.id == dl.id || it.title.equals(dl.title, ignoreCase = true) }
                if (!alreadyExists) {
                    result.add(
                        HistoryItem(
                            id = mediaId,
                            title = dl.title,
                            posterUrl = dl.posterUrl,
                            isMovie = dl.isMovie,
                            timestamp = System.currentTimeMillis()
                        )
                    )
                }
            }
            result
        }
    }

    suspend fun addToHistory(item: HistoryItem) {
        historyDao.insertHistory(item)
        auth.currentUser?.uid?.let { uid ->
            try {
                firestore.collection("users").document(uid).collection("history").document(item.id).set(item)
            } catch (e: Exception) {
                // ignore
            }
        }
    }
}