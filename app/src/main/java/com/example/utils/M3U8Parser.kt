package com.example.utils

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL
import java.net.URI

object M3U8Parser {
    
    data class QualityInfo(
        val name: String,
        val url: String
    )
    
    private fun getStandardQuality(width: Int, height: Int, rawName: String): String {
        var h = if (width > 0 && height > 0) Math.min(width, height) else Math.max(width, height)
        
        // If resolution wasn't found or is invalid, try to parse from rawName (e.g. "960p", "1080p")
        if (h <= 0) {
            val numMatch = Regex("(\\d+)[pP]").find(rawName)
            if (numMatch != null) {
                h = numMatch.groupValues[1].toIntOrNull() ?: 0
            }
        }
        
        // If still no height, check common keywords in name
        if (h <= 0) {
            val lowerName = rawName.lowercase()
            when {
                lowerName.contains("4k") || lowerName.contains("uhd") || lowerName.contains("2160") -> return "2160p"
                lowerName.contains("1440") || lowerName.contains("2k") -> return "1440p"
                lowerName.contains("1080") || lowerName.contains("fhd") -> return "1080p"
                lowerName.contains("720") || lowerName.contains("hd") -> return "720p"
                lowerName.contains("576") -> return "576p"
                lowerName.contains("480") || lowerName.contains("sd") -> return "480p"
                lowerName.contains("360") -> return "360p"
                lowerName.contains("240") -> return "240p"
                lowerName.contains("144") -> return "144p"
                else -> return rawName.ifEmpty { "Default" }
            }
        }
        
        // Map height to standard qualities
        return when {
            h >= 3800 -> "4320p"
            h >= 2000 -> "2160p"
            h >= 1300 -> "1440p"
            h >= 1000 -> "1080p"
            h >= 700 -> "720p"
            h >= 540 -> "576p"
            h >= 470 -> "480p"
            h >= 350 -> "360p"
            h >= 230 -> "240p"
            else -> "144p"
        }
    }
    
    suspend fun getQualities(masterUrl: String): List<QualityInfo> = withContext(Dispatchers.IO) {
        val qualities = mutableListOf<QualityInfo>()
        try {
            val url = URL(masterUrl)
            val conn = url.openConnection() as HttpURLConnection
            conn.connectTimeout = 5000
            conn.readTimeout = 5000
            conn.requestMethod = "GET"
            
            if (conn.responseCode == 200) {
                val content = conn.inputStream.bufferedReader().use { it.readText() }
                val lines = content.split("\n").map { it.trim() }
                
                var currentWidth = 0
                var currentHeight = 0
                var currentName = ""
                
                for (i in lines.indices) {
                    val line = lines[i]
                    if (line.startsWith("#EXT-X-STREAM-INF:")) {
                        // Extract RESOLUTION
                        val resMatch = Regex("RESOLUTION=(\\d+)x(\\d+)").find(line)
                        if (resMatch != null) {
                            currentWidth = resMatch.groupValues[1].toIntOrNull() ?: 0
                            currentHeight = resMatch.groupValues[2].toIntOrNull() ?: 0
                        }
                        
                        // Extract NAME if available
                        val nameMatch = Regex("NAME=\"([^\"]+)\"").find(line)
                        if (nameMatch != null) {
                            currentName = nameMatch.groupValues[1]
                        }
                    } else if (line.isNotEmpty() && !line.startsWith("#")) {
                        // This is the URL for the previous stream info
                        if (currentWidth > 0 || currentHeight > 0 || currentName.isNotEmpty()) {
                            val qName = getStandardQuality(currentWidth, currentHeight, currentName)
                            
                            // Resolve relative URL
                            val fullUrl = if (line.startsWith("http")) line else URI(masterUrl).resolve(line).toString()
                            qualities.add(QualityInfo(qName, fullUrl))
                        }
                        currentWidth = 0
                        currentHeight = 0
                        currentName = ""
                    }
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        
        // If no qualities parsed (maybe it's not a master playlist), return default
        if (qualities.isEmpty()) {
            qualities.add(QualityInfo("تلقائي (Default)", masterUrl))
        }
        
        // Group by name in case of duplicates (take the one with highest bandwidth if available, or just first)
        val distinctQualities = qualities.distinctBy { it.name }
        
        return@withContext distinctQualities.sortedByDescending { it.name.replace(Regex("[^0-9]"), "").toIntOrNull() ?: 0 }
    }
}