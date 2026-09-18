package com.example.utils

import android.content.Context
import java.io.File

object MediaStorageUtils {

    /**
     * Get the dedicated internal, app-private directory for downloaded movies/series/anime.
     * Stored in context.filesDir ("movies"), keeping them hidden from system gallery / file scanners.
     * Includes a .nomedia file as additional protection.
     */
    fun getMediaDirectory(context: Context): File {
        val dir = File(context.filesDir, "movies")
        if (!dir.exists()) {
            dir.mkdirs()
        }
        val noMedia = File(dir, ".nomedia")
        if (!noMedia.exists()) {
            try {
                noMedia.createNewFile()
            } catch (e: Exception) {
                // ignore
            }
        }
        return dir
    }

    /**
     * Find existing downloaded media file for a given item id across supported extensions or legacy paths.
     */
    fun findMediaFile(context: Context, id: String): File? {
        val internalDir = getMediaDirectory(context)
        
        // 1. Check in internal app directory first
        val matchingInternal = internalDir.listFiles { file ->
            file.isFile && (file.name == id || file.name.startsWith("${id}."))
        }
        if (!matchingInternal.isNullOrEmpty()) {
            return matchingInternal.first()
        }

        // 2. Check legacy external files dir (Android/data/.../files/Movies)
        val legacyExternal = context.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES)
        if (legacyExternal != null && legacyExternal.exists()) {
            val matchingExternal = legacyExternal.listFiles { file ->
                file.isFile && (file.name == id || file.name.startsWith("${id}."))
            }
            if (!matchingExternal.isNullOrEmpty()) {
                return matchingExternal.first()
            }
        }

        // 3. Check legacy downloads folder in filesDir
        val legacyDownloads = File(context.filesDir, "downloads")
        if (legacyDownloads.exists()) {
            val matchingDownloads = legacyDownloads.listFiles { file ->
                file.isFile && (file.name == id || file.name.startsWith("${id}."))
            }
            if (!matchingDownloads.isNullOrEmpty()) {
                return matchingDownloads.first()
            }
        }

        return null
    }

    /**
     * Create the destination file for a new download or transfer in internal storage,
     * preserving its original extension.
     */
    fun getDestinationFile(context: Context, id: String, extension: String? = null): File {
        val dir = getMediaDirectory(context)
        val cleanExt = extension?.trim()?.removePrefix(".")?.ifEmpty { null }
        val fileName = if (cleanExt != null) "${id}.${cleanExt}" else "${id}.mp4"
        return File(dir, fileName)
    }
}
