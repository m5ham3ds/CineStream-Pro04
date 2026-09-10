package com.example.data.repository

import android.content.Context
import com.example.data.db.AppDatabase
import com.example.data.model.LibraryItem
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.Flow

class LibraryRepository(context: Context) {
    private val db = AppDatabase.getDatabase(context)
    private val libraryDao = db.libraryDao()
    private val auth = FirebaseAuth.getInstance()
    private val firestore = FirebaseFirestore.getInstance()

    fun isItemInLibrary(id: String): Flow<Boolean> = libraryDao.isItemInLibrary(id)

    fun getLibraryItems(): Flow<List<LibraryItem>> {
        return libraryDao.getAllItems()
    }

    suspend fun addToLibrary(item: LibraryItem) {
        libraryDao.insertItem(item)
        auth.currentUser?.uid?.let { uid ->
            try {
                firestore.collection("users").document(uid).collection("library").document(item.id).set(item)
            } catch (e: Exception) {
                // ignore
            }
        }
    }

    suspend fun removeFromLibrary(item: LibraryItem) {
        libraryDao.deleteItem(item)
        auth.currentUser?.uid?.let { uid ->
            try {
                firestore.collection("users").document(uid).collection("library").document(item.id).delete()
            } catch (e: Exception) {
                // ignore
            }
        }
    }
}
