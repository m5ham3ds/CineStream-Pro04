package com.example.data.sync

import android.content.Context
import com.example.data.db.AppDatabase
import com.example.data.model.HistoryItem
import com.example.data.model.LibraryItem
import com.example.data.model.WatchedEpisode
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.tasks.await

class CloudSyncManager(context: Context) {
    private val db = AppDatabase.getDatabase(context)
    private val firestore = FirebaseFirestore.getInstance()

    suspend fun syncFromCloud(userId: String) {
        val userDoc = firestore.collection("users").document(userId)
        
        try {
            // Watchlist
            val librarySnapshot = userDoc.collection("library").get().await()
            val libraryItems = librarySnapshot.toObjects(LibraryItem::class.java)
            libraryItems.forEach { db.libraryDao().insertItem(it) }

            // History
            val historySnapshot = userDoc.collection("history").get().await()
            val historyItems = historySnapshot.toObjects(HistoryItem::class.java)
            historyItems.forEach { db.historyDao().insertHistory(it) }

            // Watched Episodes
            val episodesSnapshot = userDoc.collection("watched_episodes").get().await()
            val episodes = episodesSnapshot.toObjects(WatchedEpisode::class.java)
            episodes.forEach { db.watchedEpisodeDao().insert(it) }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    suspend fun clearLocalData() {
        db.libraryDao().clearAll()
        db.historyDao().clearAll()
        db.watchedEpisodeDao().clearAll()
    }
}
