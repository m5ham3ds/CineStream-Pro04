package com.example.utils

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build

object NetworkUtils {
    fun getEstimatedBandwidthKbps(context: Context): Int {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val network = cm.activeNetwork ?: return 2000 // Default 2Mbps
            val caps = cm.getNetworkCapabilities(network) ?: return 2000
            return caps.linkDownstreamBandwidthKbps
        }
        return 2000 // Default fallback
    }

    fun selectBestQuality(qualities: List<M3U8Parser.QualityInfo>, bandwidthKbps: Int): M3U8Parser.QualityInfo {
        if (qualities.isEmpty()) return M3U8Parser.QualityInfo("Auto", "")
        if (qualities.size == 1) return qualities.first()

        val targetHeight = when {
            bandwidthKbps >= 15000 -> 2160
            bandwidthKbps >= 5000 -> 1080
            bandwidthKbps >= 2500 -> 720
            bandwidthKbps >= 1000 -> 480
            else -> 360
        }

        val sortedQualities = qualities.sortedByDescending { it.name.replace(Regex("[^0-9]"), "").toIntOrNull() ?: 0 }
        
        for (q in sortedQualities) {
            val h = q.name.replace(Regex("[^0-9]"), "").toIntOrNull() ?: 0
            if (h <= targetHeight && h > 0) {
                return q
            }
        }
        
        return sortedQualities.lastOrNull() ?: qualities.first()
    }

    fun isInternetAvailable(context: Context): Boolean {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val network = connectivityManager.activeNetwork ?: return false
            val activeNetwork = connectivityManager.getNetworkCapabilities(network) ?: return false
            return when {
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> true
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> true
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) -> true
                else -> false
            }
        } else {
            @Suppress("DEPRECATION")
            val networkInfo = connectivityManager.activeNetworkInfo ?: return false
            @Suppress("DEPRECATION")
            return networkInfo.isConnected
        }
    }
}
