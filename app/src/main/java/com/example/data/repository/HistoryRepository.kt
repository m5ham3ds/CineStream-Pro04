package com.example.data.repository

import android.content.Context
import com.example.data.db.AppDatabase
import com.example.data.model.HistoryItem
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.Flow

class HistoryRepository(context: Context) {
    private val db = AppDatabase.getDatabase(context)
    private val historyDao = db.historyDao()
    private val auth = FirebaseAuth.getInstance()
    private val firestore = FirebaseFirestore.getInstance()

    fun getHistoryItems(): Flow<List<HistoryItem>> = historyDao.getAllHistory()

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
