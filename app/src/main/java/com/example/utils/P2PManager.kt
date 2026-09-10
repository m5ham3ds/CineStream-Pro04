package com.example.utils

import android.content.Context
import com.google.android.gms.nearby.Nearby
import com.google.android.gms.nearby.connection.AdvertisingOptions
import com.google.android.gms.nearby.connection.ConnectionInfo
import com.google.android.gms.nearby.connection.ConnectionLifecycleCallback
import com.google.android.gms.nearby.connection.ConnectionResolution
import com.google.android.gms.nearby.connection.ConnectionsStatusCodes
import com.google.android.gms.nearby.connection.DiscoveredEndpointInfo
import com.google.android.gms.nearby.connection.DiscoveryOptions
import com.google.android.gms.nearby.connection.EndpointDiscoveryCallback
import com.google.android.gms.nearby.connection.Payload
import com.google.android.gms.nearby.connection.PayloadCallback
import com.google.android.gms.nearby.connection.PayloadTransferUpdate
import com.google.android.gms.nearby.connection.Strategy
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.io.File
import org.json.JSONObject

enum class P2PState {
    IDLE, ADVERTISING, DISCOVERING, CONNECTED, TRANSFERRING
}

data class Endpoint(val id: String, val name: String)

class P2PManager(private val context: Context) {
    private val connectionsClient = Nearby.getConnectionsClient(context)
    private val STRATEGY = Strategy.P2P_POINT_TO_POINT
    private val SERVICE_ID = "com.example.cinestream.P2P"

    private val _p2pState = MutableStateFlow(P2PState.IDLE)
    val p2pState: StateFlow<P2PState> = _p2pState.asStateFlow()

    private val _discoveredEndpoints = MutableStateFlow<List<Endpoint>>(emptyList())
    val discoveredEndpoints: StateFlow<List<Endpoint>> = _discoveredEndpoints.asStateFlow()

    private val _connectedEndpoint = MutableStateFlow<Endpoint?>(null)
    val connectedEndpoint: StateFlow<Endpoint?> = _connectedEndpoint.asStateFlow()
    
    private val _transferProgress = MutableStateFlow(0f)
    val transferProgress = _transferProgress.asStateFlow()

    var onMovieReceived: ((String, String, Boolean, String) -> Unit)? = null // id, title, isMovie, posterUrl // id, title, isMovie

    // Key: Payload ID, Value: File path/info
    private val incomingFilePayloads = mutableMapOf<Long, File>()

    fun startAdvertising(userName: String) {
        val advertisingOptions = AdvertisingOptions.Builder().setStrategy(STRATEGY).build()
        connectionsClient.startAdvertising(
            userName, SERVICE_ID, connectionLifecycleCallback, advertisingOptions
        ).addOnSuccessListener {
            _p2pState.value = P2PState.ADVERTISING
        }.addOnFailureListener {
            _p2pState.value = P2PState.IDLE
        }
    }

    fun startDiscovery() {
        val discoveryOptions = DiscoveryOptions.Builder().setStrategy(STRATEGY).build()
        _discoveredEndpoints.value = emptyList()
        connectionsClient.startDiscovery(
            SERVICE_ID, endpointDiscoveryCallback, discoveryOptions
        ).addOnSuccessListener {
            _p2pState.value = P2PState.DISCOVERING
        }.addOnFailureListener {
            _p2pState.value = P2PState.IDLE
        }
    }

    fun requestConnection(endpointId: String, userName: String) {
        connectionsClient.requestConnection(userName, endpointId, connectionLifecycleCallback)
    }

    fun stopAll() {
        connectionsClient.stopAdvertising()
        connectionsClient.stopDiscovery()
        connectionsClient.stopAllEndpoints()
        _p2pState.value = P2PState.IDLE
        _connectedEndpoint.value = null
        _discoveredEndpoints.value = emptyList()
    }

    fun sendMovie(endpointId: String, movieId: String, title: String, isMovie: Boolean, posterUrl: String, file: File) {
        try {
            // 1. Send Metadata as bytes
            val metadata = JSONObject()
            metadata.put("type", "metadata")
            metadata.put("id", movieId)
            metadata.put("title", title)
            metadata.put("isMovie", isMovie)
            metadata.put("posterUrl", posterUrl)
            val metadataPayload = Payload.fromBytes(metadata.toString().toByteArray())
            connectionsClient.sendPayload(endpointId, metadataPayload)

            // 2. Send the actual file
            val filePayload = Payload.fromFile(file)
            connectionsClient.sendPayload(endpointId, filePayload)
            _p2pState.value = P2PState.TRANSFERRING
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private val endpointDiscoveryCallback = object : EndpointDiscoveryCallback() {
        override fun onEndpointFound(endpointId: String, info: DiscoveredEndpointInfo) {
            val current = _discoveredEndpoints.value.toMutableList()
            current.add(Endpoint(endpointId, info.endpointName))
            _discoveredEndpoints.value = current
        }

        override fun onEndpointLost(endpointId: String) {
            val current = _discoveredEndpoints.value.toMutableList()
            current.removeAll { it.id == endpointId }
            _discoveredEndpoints.value = current
        }
    }

    private var incomingMetadata: JSONObject? = null

    private val payloadCallback = object : PayloadCallback() {
        override fun onPayloadReceived(endpointId: String, payload: Payload) {
            if (payload.type == Payload.Type.BYTES) {
                val data = payload.asBytes()
                if (data != null) {
                    val json = JSONObject(String(data))
                    if (json.optString("type") == "metadata") {
                        incomingMetadata = json
                    }
                }
            } else if (payload.type == Payload.Type.FILE) {
                val file = payload.asFile()?.asJavaFile()
                if (file != null) {
                    incomingFilePayloads[payload.id] = file
                }
            }
        }

        override fun onPayloadTransferUpdate(endpointId: String, update: PayloadTransferUpdate) {
            if (update.status == PayloadTransferUpdate.Status.IN_PROGRESS) {
                _p2pState.value = P2PState.TRANSFERRING
                _transferProgress.value = update.bytesTransferred.toFloat() / update.totalBytes.toFloat()
            } else if (update.status == PayloadTransferUpdate.Status.SUCCESS) {
                _p2pState.value = P2PState.CONNECTED
                _transferProgress.value = 1f
                
                // Handle file success
                val payloadFile = incomingFilePayloads[update.payloadId]
                if (payloadFile != null && incomingMetadata != null) {
                    val id = incomingMetadata!!.getString("id")
                    val title = incomingMetadata!!.getString("title")
                    val isMovie = incomingMetadata!!.getBoolean("isMovie")
                    
                    // Move file to our downloads directory
                    val destDir = File(context.filesDir, "downloads")
                    if (!destDir.exists()) destDir.mkdirs()
                    val destFile = File(destDir, "${id}.mp4")
                    
                    payloadFile.copyTo(destFile, overwrite = true)
                    
                    val posterUrl = incomingMetadata!!.optString("posterUrl", "")
                    onMovieReceived?.invoke(id, title, isMovie, posterUrl)
                    
                    incomingMetadata = null
                    incomingFilePayloads.remove(update.payloadId)
                }
            }
        }
    }

    private val connectionLifecycleCallback = object : ConnectionLifecycleCallback() {
        override fun onConnectionInitiated(endpointId: String, info: ConnectionInfo) {
            // Automatically accept
            connectionsClient.acceptConnection(endpointId, payloadCallback)
        }

        override fun onConnectionResult(endpointId: String, result: ConnectionResolution) {
            if (result.status.statusCode == ConnectionsStatusCodes.STATUS_OK) {
                connectionsClient.stopDiscovery()
                connectionsClient.stopAdvertising()
                _p2pState.value = P2PState.CONNECTED
                _connectedEndpoint.value = Endpoint(endpointId, "Connected Device") // We can store actual name if we cache it
            } else {
                _p2pState.value = P2PState.IDLE
            }
        }

        override fun onDisconnected(endpointId: String) {
            if (_connectedEndpoint.value?.id == endpointId) {
                _p2pState.value = P2PState.IDLE
                _connectedEndpoint.value = null
            }
        }
    }
}
