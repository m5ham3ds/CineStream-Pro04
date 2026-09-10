package com.example.data.model
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "history_items")
data class HistoryItem(
    @PrimaryKey val id: String,
    val title: String,
    val posterUrl: String,
    val isMovie: Boolean,
    val timestamp: Long = System.currentTimeMillis()
)
