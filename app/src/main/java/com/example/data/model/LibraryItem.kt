package com.example.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "library_items")
data class LibraryItem(
    @PrimaryKey val id: String,
    val title: String,
    val posterUrl: String,
    val isMovie: Boolean
)
