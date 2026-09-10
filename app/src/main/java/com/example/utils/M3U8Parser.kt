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
                
                var currentResolution = ""
                var currentName = ""
                
                for (i in lines.indices) {
                    val line = lines[i]
                    if (line.startsWith("#EXT-X-STREAM-INF:")) {
                        // Extract RESOLUTION
                        val resMatch = Regex("RESOLUTION=\\d+x(\\d+)").find(line)
                        if (resMatch != null) {
                            currentResolution = "${resMatch.groupValues[1]}p"
                        }
                        
                        // Extract NAME if available
                        val nameMatch = Regex("NAME=\"([^\"]+)\"").find(line)
                        if (nameMatch != null) {
                            currentName = nameMatch.groupValues[1]
                        }
                    } else if (line.isNotEmpty() && !line.startsWith("#")) {
                        // This is the URL for the previous stream info
                        if (currentResolution.isNotEmpty() || currentName.isNotEmpty()) {
                            val qName = currentName.ifEmpty { currentResolution }.ifEmpty { "Default" }
                            // Resolve relative URL
                            val fullUrl = if (line.startsWith("http")) line else URI(masterUrl).resolve(line).toString()
                            qualities.add(QualityInfo(qName, fullUrl))
                        }
                        currentResolution = ""
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
        
        return@withContext qualities.distinctBy { it.name }.sortedByDescending { it.name.replace(Regex("[^0-9]"), "").toIntOrNull() ?: 0 }
    }
}
