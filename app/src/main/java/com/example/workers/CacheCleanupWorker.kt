package com.example.workers

import android.content.Context
import android.util.Log
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import coil.imageLoader
import java.io.File

class CacheCleanupWorker(
    private val context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        return try {
            Log.d("CacheCleanupWorker", "Starting cache cleanup...")
            
            // 1. Clear Coil Disk Cache (Images/Covers)
            context.imageLoader.diskCache?.clear()
            context.imageLoader.memoryCache?.clear()
            
            // 2. Clear application cache directory if needed, but safely
            val cacheDir = context.cacheDir
            if (cacheDir != null && cacheDir.exists()) {
                val okHttpCache = File(cacheDir, "http_cache")
                if (okHttpCache.exists()) {
                    okHttpCache.deleteRecursively()
                }
            }
            
            Log.d("CacheCleanupWorker", "Cache cleanup completed successfully.")
            Result.success()
        } catch (e: Exception) {
            Log.e("CacheCleanupWorker", "Error cleaning cache", e)
            Result.failure()
        }
    }
}
