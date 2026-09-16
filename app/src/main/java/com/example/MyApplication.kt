package com.example

import android.app.Application
import coil.ImageLoader
import coil.ImageLoaderFactory
import coil.disk.DiskCache
import coil.memory.MemoryCache
import okhttp3.Cache
import java.io.File

class MyApplication : Application(), ImageLoaderFactory {
    companion object {
        lateinit var appContext: android.content.Context
    }

    
    override fun onCreate() {
        super.onCreate()
        appContext = applicationContext

        
        val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
            val stackTrace = android.util.Log.getStackTraceString(throwable)
            val intent = android.content.Intent(this, com.example.ui.screens.crash.CrashActivity::class.java).apply {
                putExtra("EXTRA_STACK_TRACE", stackTrace)
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK
            }
            startActivity(intent)
            android.os.Process.killProcess(android.os.Process.myPid())
            System.exit(1)
        }

        com.example.di.AppContainer.application = this
        
        val cloudName = com.example.BuildConfig.CLOUDINARY_CLOUD_NAME
        if (cloudName.isNotEmpty()) {
            val config = mapOf(
                "cloud_name" to cloudName
            )
            try {
                com.cloudinary.android.MediaManager.init(this, config)
            } catch (e: Exception) {
                // Ignore if already initialized
            }
        }

    }

    override fun newImageLoader(): ImageLoader {
        return ImageLoader.Builder(this)
            .memoryCache {
                MemoryCache.Builder(this)
                    .maxSizePercent(0.25)
                    .build()
            }
            .diskCache {
                DiskCache.Builder()
                    .directory(this.cacheDir.resolve("image_cache"))
                    .maxSizePercent(0.05) // 5% of total disk space
                    .build()
            }
            .crossfade(true)
            .respectCacheHeaders(false) // Ignore server headers that say don't cache
            .build()
    }
}