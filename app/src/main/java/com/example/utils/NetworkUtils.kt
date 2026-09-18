package com.example.utils

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.net.wifi.WifiManager
import java.net.Inet4Address
import java.net.NetworkInterface
import java.util.Collections

object NetworkUtils {

    fun isInternetAvailable(context: Context): Boolean {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as? ConnectivityManager ?: return false
        val activeNetwork = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(activeNetwork) ?: return false
        return capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    }

    fun getEstimatedBandwidthKbps(context: Context): Int {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as? ConnectivityManager ?: return 5000
        val activeNetwork = connectivityManager.activeNetwork ?: return 5000
        val capabilities = connectivityManager.getNetworkCapabilities(activeNetwork) ?: return 5000
        val downstream = capabilities.linkDownstreamBandwidthKbps
        return if (downstream > 0) downstream else 5000
    }

    fun selectBestQuality(qualities: List<M3U8Parser.QualityInfo>, bandwidthKbps: Int): M3U8Parser.QualityInfo {
        if (qualities.isEmpty()) {
            return M3U8Parser.QualityInfo("Auto", "")
        }
        return when {
            bandwidthKbps >= 5000 -> qualities.find { it.name.contains("1080") } ?: qualities.first()
            bandwidthKbps >= 2500 -> qualities.find { it.name.contains("720") } ?: qualities.first()
            bandwidthKbps >= 1000 -> qualities.find { it.name.contains("480") } ?: qualities.first()
            else -> qualities.find { it.name.contains("360") } ?: qualities.last()
        }
    }

    fun getLocalIpAddress(context: Context? = null): String {
        try {
            val interfaces = Collections.list(NetworkInterface.getNetworkInterfaces())
            for (intf in interfaces) {
                if (!intf.isUp || intf.isLoopback) continue
                val addrs = Collections.list(intf.inetAddresses)
                for (addr in addrs) {
                    if (!addr.isLoopbackAddress && addr is Inet4Address) {
                        val host = addr.hostAddress ?: continue
                        if (!host.startsWith("127.")) {
                            return host
                        }
                    }
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        if (context != null) {
            try {
                val wifiManager = context.applicationContext.getSystemService(Context.WIFI_SERVICE) as? WifiManager
                val ipInt = wifiManager?.connectionInfo?.ipAddress ?: 0
                if (ipInt != 0) {
                    return String.format(
                        "%d.%d.%d.%d",
                        ipInt and 0xff,
                        ipInt shr 8 and 0xff,
                        ipInt shr 16 and 0xff,
                        ipInt shr 24 and 0xff
                    )
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        return "127.0.0.1"
    }
}
