package com.example.data.db

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.data.model.LibraryItem
import kotlinx.coroutines.flow.Flow

@Dao
interface LibraryDao {
    @Query("SELECT * FROM library_items")
    fun getAllItems(): Flow<List<LibraryItem>>

    @Query("SELECT EXISTS(SELECT * FROM library_items WHERE id = :id)")
    fun isItemInLibrary(id: String): Flow<Boolean>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertItem(item: LibraryItem)

    @Delete
    suspend fun deleteItem(item: LibraryItem)
    @Query("DELETE FROM library_items")
    suspend fun clearAll()
}
