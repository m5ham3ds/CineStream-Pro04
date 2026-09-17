package com.example.data.repository

import android.content.Context
import com.example.data.db.AppDatabase
import com.example.data.model.NotificationItem
import kotlinx.coroutines.flow.Flow

class NotificationRepository(context: Context) {
    private val notificationDao = AppDatabase.getDatabase(context).notificationDao()

    fun getAllNotifications(): Flow<List<NotificationItem>> = notificationDao.getAllNotifications()

    fun getUnreadCount(): Flow<Int> = notificationDao.getUnreadCount()

    suspend fun addNotification(title: String, message: String, imageUrl: String? = null, type: String = "info") {
        val notification = NotificationItem(
            title = title,
            message = message,
            imageUrl = imageUrl,
            type = type
        )
        notificationDao.insertNotification(notification)
    }

    suspend fun markAllAsRead() {
        notificationDao.markAllAsRead()
    }
    
    suspend fun markAsRead(id: String) {
        notificationDao.markAsRead(id)
    }

    suspend fun deleteNotification(id: String) {
        notificationDao.deleteNotification(id)
    }
}
