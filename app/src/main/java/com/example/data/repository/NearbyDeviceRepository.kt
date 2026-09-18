package com.example.data.repository

import android.content.Context
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import org.json.JSONArray
import org.json.JSONObject

data class NearbyDevice(
    val id: String,
    val name: String,
    val ip: String? = null,
    val port: Int = 8888,
    val isConnected: Boolean = false,
    val lastSeen: Long = System.currentTimeMillis()
)

class NearbyDeviceRepository(context: Context) {
    private val prefs = context.getSharedPreferences("p2p_remembered_devices", Context.MODE_PRIVATE)
    private val _devices = MutableStateFlow<List<NearbyDevice>>(emptyList())
    val devices: StateFlow<List<NearbyDevice>> = _devices.asStateFlow()

    init {
        loadDevices()
    }

    private fun loadDevices() {
        val raw = prefs.getString("devices_json", null) ?: "[]"
        try {
            val arr = JSONArray(raw)
            val list = mutableListOf<NearbyDevice>()
            for (i in 0 until arr.length()) {
                val obj = arr.getJSONObject(i)
                val rawIp = obj.optString("ip", "").trim()
                list.add(
                    NearbyDevice(
                        id = obj.getString("id"),
                        name = obj.getString("name"),
                        ip = if (rawIp.isNotEmpty() && rawIp != "null") rawIp else null,
                        port = obj.optInt("port", 8888),
                        isConnected = false, // Always start as disconnected on app launch
                        lastSeen = obj.optLong("lastSeen", System.currentTimeMillis())
                    )
                )
            }
            _devices.value = list
        } catch (e: Exception) {
            _devices.value = emptyList()
        }
    }

    fun addOrUpdateDevice(device: NearbyDevice) {
        val current = _devices.value.toMutableList()
        val existing = current.find { it.id == device.id || it.name == device.name }
        val finalDevice = if (device.ip.isNullOrBlank() && !existing?.ip.isNullOrBlank()) {
            device.copy(ip = existing?.ip)
        } else {
            device
        }
        current.removeAll { it.id == finalDevice.id || it.name == finalDevice.name }
        current.add(0, finalDevice)
        _devices.value = current
        saveDevices(current)
    }

    fun setDeviceConnected(idOrName: String, isConnected: Boolean) {
        val current = _devices.value.toMutableList()
        val index = current.indexOfFirst { it.id == idOrName || it.name == idOrName }
        if (index != -1) {
            val updated = current[index].copy(isConnected = isConnected, lastSeen = System.currentTimeMillis())
            current[index] = updated
            _devices.value = current
            saveDevices(current)
        }
    }

    fun setAllDisconnected() {
        val current = _devices.value.map { it.copy(isConnected = false) }
        _devices.value = current
        saveDevices(current)
    }

    private fun saveDevices(list: List<NearbyDevice>) {
        val arr = JSONArray()
        list.take(20).forEach { item ->
            val obj = JSONObject()
            obj.put("id", item.id)
            obj.put("name", item.name)
            obj.put("ip", item.ip ?: "")
            obj.put("port", item.port)
            obj.put("lastSeen", item.lastSeen)
            arr.put(obj)
        }
        prefs.edit().putString("devices_json", arr.toString()).apply()
    }
}
