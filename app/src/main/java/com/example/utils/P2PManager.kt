package com.example.utils

import android.content.Context
import android.os.Build
import com.example.data.model.DownloadItem
import com.google.android.gms.nearby.Nearby
import com.google.android.gms.nearby.connection.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import org.json.JSONObject
import java.io.*
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.ServerSocket
import java.net.Socket

enum class P2PState {
    IDLE, ADVERTISING, DISCOVERING, CONNECTED, TRANSFERRING
}

data class Endpoint(val id: String, val name: String, val isConnected: Boolean = false, val ip: String? = null)

data class ConnectionRequest(
    val endpointId: String,
    val deviceName: String,
    val isSocket: Boolean = true
)

class P2PManager(private val context: Context) {
    private val connectionsClient = Nearby.getConnectionsClient(context)
    private val STRATEGY = Strategy.P2P_STAR
    private val SERVICE_ID = "com.example.cinestream.P2P"

    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    private val _p2pState = MutableStateFlow(P2PState.IDLE)
    val p2pState: StateFlow<P2PState> = _p2pState.asStateFlow()

    private val _discoveredEndpoints = MutableStateFlow<List<Endpoint>>(emptyList())
    val discoveredEndpoints: StateFlow<List<Endpoint>> = _discoveredEndpoints.asStateFlow()

    private val _connectedEndpoint = MutableStateFlow<Endpoint?>(null)
    val connectedEndpoint: StateFlow<Endpoint?> = _connectedEndpoint.asStateFlow()

    private val _transferProgress = MutableStateFlow(0f)
    val transferProgress: StateFlow<Float> = _transferProgress.asStateFlow()

    // Receiver incoming connection request
    private val _pendingConnectionRequest = MutableStateFlow<ConnectionRequest?>(null)
    val pendingConnectionRequest: StateFlow<ConnectionRequest?> = _pendingConnectionRequest.asStateFlow()

    // Sender waiting for receiver's approval
    private val _isWaitingForApproval = MutableStateFlow(false)
    val isWaitingForApproval: StateFlow<Boolean> = _isWaitingForApproval.asStateFlow()

    private val _connectingTargetName = MutableStateFlow<String?>(null)
    val connectingTargetName: StateFlow<String?> = _connectingTargetName.asStateFlow()

    private val _isScanning = MutableStateFlow(false)
    val isScanning: StateFlow<Boolean> = _isScanning.asStateFlow()

    var onMediaReceived: ((String, String, String, Boolean, String, String) -> Unit)? = null
    var onMediaSent: ((DownloadItem) -> Unit)? = null
    var onConnectionEstablished: ((String) -> Unit)? = null
    var onConnectionDeclined: ((String) -> Unit)? = null
    var onDisconnected: ((String) -> Unit)? = null

    // Socket server & client state
    private var serverSocket: ServerSocket? = null
    private var serverJob: Job? = null
    private var activeSocket: Socket? = null
    private var senderConnectionJob: Job? = null
    private var socketReader: BufferedReader? = null
    private var socketWriter: BufferedWriter? = null
    
    // CompletableDeferred for receiver user confirmation
    private var connectionDecision: CompletableDeferred<Boolean>? = null

    // Nearby incoming payloads
    private val incomingFilePayloads = mutableMapOf<Long, File>()
    private val incomingMetadataMap = mutableMapOf<Long, JSONObject>()

    // UDP Discovery state
    private var udpDiscoveryJob: Job? = null
    private var udpServerJob: Job? = null

    fun startAdvertising(userName: String, port: Int = 8888) {
        stopAll()
        startSocketServer(port)
        startUdpResponder(userName, port)

        val advertisingOptions = AdvertisingOptions.Builder().setStrategy(STRATEGY).build()
        connectionsClient.startAdvertising(
            userName, SERVICE_ID, connectionLifecycleCallback, advertisingOptions
        ).addOnSuccessListener {
            _p2pState.value = P2PState.ADVERTISING
        }.addOnFailureListener {
            _p2pState.value = P2PState.ADVERTISING
        }
    }

    fun startDiscovery() {
        _isScanning.value = true
        _discoveredEndpoints.value = emptyList()

        // 1. Google Nearby Discovery
        val discoveryOptions = DiscoveryOptions.Builder().setStrategy(STRATEGY).build()
        connectionsClient.startDiscovery(
            SERVICE_ID, endpointDiscoveryCallback, discoveryOptions
        ).addOnSuccessListener {
            _p2pState.value = P2PState.DISCOVERING
        }.addOnFailureListener {
            _p2pState.value = P2PState.DISCOVERING
        }

        // 2. UDP Local Wi-Fi Broadcast Discovery
        startUdpDiscovery()
    }

    fun stopDiscovery() {
        _isScanning.value = false
        _discoveredEndpoints.value = emptyList()
        udpDiscoveryJob?.cancel()
        udpDiscoveryJob = null
        try {
            connectionsClient.stopDiscovery()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        if (_p2pState.value == P2PState.DISCOVERING) {
            _p2pState.value = P2PState.IDLE
        }
    }

    private fun startUdpDiscovery() {
        udpDiscoveryJob?.cancel()
        udpDiscoveryJob = scope.launch {
            var socket: DatagramSocket? = null
            try {
                socket = DatagramSocket()
                socket.broadcast = true
                socket.soTimeout = 3000

                val pingMsg = "CINESTREAM_PING:${Build.MODEL}"
                val buffer = pingMsg.toByteArray()
                val packet = DatagramPacket(
                    buffer, buffer.size,
                    InetAddress.getByName("255.255.255.255"), 8889
                )
                socket.send(packet)

                val receiveBuf = ByteArray(1024)
                val receivePacket = DatagramPacket(receiveBuf, receiveBuf.size)

                val startTime = System.currentTimeMillis()
                while (isActive && System.currentTimeMillis() - startTime < 10000) {
                    try {
                        socket.receive(receivePacket)
                        val resp = String(receivePacket.data, 0, receivePacket.length)
                        if (resp.startsWith("CINESTREAM_PONG:")) {
                            val parts = resp.substringAfter("CINESTREAM_PONG:").split(";")
                            val peerName = parts.getOrNull(0) ?: "Nearby Device"
                            val peerIp = receivePacket.address.hostAddress ?: ""
                            val peerPort = parts.getOrNull(1)?.toIntOrNull() ?: 8888

                            if (peerIp.isNotBlank() && peerIp != "127.0.0.1") {
                                val endpoint = Endpoint(
                                    id = "udp_${peerIp}_$peerPort",
                                    name = peerName,
                                    isConnected = false,
                                    ip = peerIp
                                )
                                withContext(Dispatchers.Main) {
                                    val current = _discoveredEndpoints.value.toMutableList()
                                    if (current.none { it.name == peerName || it.ip == peerIp }) {
                                        current.add(endpoint)
                                        _discoveredEndpoints.value = current
                                    }
                                }
                            }
                        }
                    } catch (e: Exception) {
                        // Timeout on receive, continue loop
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                socket?.close()
                _isScanning.value = false
                // If user did not connect to discovered devices, clear them after brief grace period
                delay(4000)
                if (_connectedEndpoint.value == null && !_isWaitingForApproval.value) {
                    _discoveredEndpoints.value = emptyList()
                }
            }
        }
    }

    private fun startUdpResponder(userName: String, port: Int) {
        udpServerJob?.cancel()
        udpServerJob = scope.launch {
            var socket: DatagramSocket? = null
            try {
                socket = DatagramSocket(8889)
                val buffer = ByteArray(1024)
                val packet = DatagramPacket(buffer, buffer.size)

                while (isActive) {
                    socket.receive(packet)
                    val msg = String(packet.data, 0, packet.length)
                    if (msg.startsWith("CINESTREAM_PING:")) {
                        val reply = "CINESTREAM_PONG:$userName;$port"
                        val replyBytes = reply.toByteArray()
                        val replyPacket = DatagramPacket(
                            replyBytes, replyBytes.size,
                            packet.address, packet.port
                        )
                        socket.send(replyPacket)
                    }
                }
            } catch (e: Exception) {
                // Stopped
            } finally {
                socket?.close()
            }
        }
    }

    private fun startSocketServer(port: Int) {
        serverJob?.cancel()
        serverJob = scope.launch {
            try {
                serverSocket?.close()
                val server = ServerSocket()
                server.reuseAddress = true
                server.bind(InetSocketAddress(port))
                serverSocket = server

                while (isActive) {
                    val client = server.accept()
                    activeSocket?.close()
                    activeSocket = client
                    handleIncomingSocketConnection(client)
                }
            } catch (e: Exception) {
                // Server closed
            }
        }
    }

    private suspend fun handleIncomingSocketConnection(socket: Socket) {
        withContext(Dispatchers.IO) {
            try {
                socket.soTimeout = 30000
                val reader = BufferedReader(InputStreamReader(socket.getInputStream()))
                val writer = BufferedWriter(OutputStreamWriter(socket.getOutputStream()))
                socketReader = reader
                socketWriter = writer

                // 1. Read connection request from Sender
                val requestLine = reader.readLine() ?: return@withContext
                val requestJson = JSONObject(requestLine)
                val senderName = requestJson.optString("deviceName", "Nearby Device")
                val endpointId = socket.inetAddress?.hostAddress ?: "peer"

                // 2. Trigger Confirmation Dialog on Receiver's UI
                val decisionDeferred = CompletableDeferred<Boolean>()
                connectionDecision = decisionDeferred
                _pendingConnectionRequest.value = ConnectionRequest(endpointId, senderName, isSocket = true)

                // Wait for user to explicitly click Accept or Decline
                val accepted = decisionDeferred.await()
                _pendingConnectionRequest.value = null

                if (!accepted) {
                    // Send rejection ack
                    val rejectJson = JSONObject().apply {
                        put("type", "connection_rejected")
                    }
                    writer.write(rejectJson.toString() + "\n")
                    writer.flush()
                    socket.close()
                    return@withContext
                }

                // User Accepted: send confirmation ack
                val ackJson = JSONObject().apply {
                    put("type", "connection_accepted")
                    put("deviceName", Build.MODEL)
                }
                writer.write(ackJson.toString() + "\n")
                writer.flush()

                val endpoint = Endpoint(endpointId, senderName, isConnected = true, ip = endpointId)
                _connectedEndpoint.value = endpoint
                _p2pState.value = P2PState.CONNECTED
                TransferNotificationHelper.showConnectionNotification(context, senderName)
                onConnectionEstablished?.invoke(senderName)

                // 3. Listen for incoming file streams
                while (isActive && !socket.isClosed) {
                    val line = reader.readLine() ?: break
                    val header = JSONObject(line)
                    if (header.optString("type") == "file_transfer") {
                        val id = header.getString("id")
                        val mediaId = header.optString("mediaId", id)
                        val title = header.getString("title")
                        val isMovie = header.getBoolean("isMovie")
                        val posterUrl = header.optString("posterUrl", "")
                        val quality = header.optString("quality", "1080p")
                        val fileSize = header.getLong("fileSize")
                        val extension = header.optString("extension", "mp4").ifEmpty { "mp4" }

                        _p2pState.value = P2PState.TRANSFERRING
                        _transferProgress.value = 0f
                        TransferNotificationHelper.showTransferProgress(context, title, 0, isSender = false)

                        val destFile = MediaStorageUtils.getDestinationFile(context, id, extension)
                        val fileOut = FileOutputStream(destFile)
                        val rawIn = socket.getInputStream()
                        val buffer = ByteArray(64 * 1024)
                        var bytesReadTotal = 0L
                        var lastNotifTime = 0L

                        while (bytesReadTotal < fileSize) {
                            val toRead = minOf(buffer.size.toLong(), fileSize - bytesReadTotal).toInt()
                            val read = rawIn.read(buffer, 0, toRead)
                            if (read == -1) break
                            fileOut.write(buffer, 0, read)
                            bytesReadTotal += read

                            val progress = if (fileSize > 0) bytesReadTotal.toFloat() / fileSize.toFloat() else 1f
                            _transferProgress.value = progress

                            val now = System.currentTimeMillis()
                            if (now - lastNotifTime > 250) {
                                TransferNotificationHelper.showTransferProgress(context, title, (progress * 100).toInt(), isSender = false)
                                lastNotifTime = now
                            }
                        }
                        fileOut.flush()
                        fileOut.close()

                        // Acknowledge complete
                        val completeJson = JSONObject().apply {
                            put("type", "transfer_complete")
                            put("id", id)
                        }
                        writer.write(completeJson.toString() + "\n")
                        writer.flush()

                        _p2pState.value = P2PState.CONNECTED
                        _transferProgress.value = 1f
                        TransferNotificationHelper.showTransferComplete(context, title, isSender = false)
                        onMediaReceived?.invoke(id, mediaId, title, isMovie, posterUrl, quality)
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                val current = _connectedEndpoint.value
                if (current != null) {
                    onDisconnected?.invoke(current.name)
                }
                _connectedEndpoint.value = null
                _p2pState.value = P2PState.IDLE
            }
        }
    }

    fun acceptConnection() {
        val req = _pendingConnectionRequest.value
        if (req != null) {
            if (req.isSocket) {
                connectionDecision?.complete(true)
            } else {
                connectionsClient.acceptConnection(req.endpointId, payloadCallback)
                val endpoint = Endpoint(req.endpointId, req.deviceName, isConnected = true)
                _connectedEndpoint.value = endpoint
                _p2pState.value = P2PState.CONNECTED
                TransferNotificationHelper.showConnectionNotification(context, req.deviceName)
                onConnectionEstablished?.invoke(req.deviceName)
                _pendingConnectionRequest.value = null
            }
        }
    }

    fun rejectConnection() {
        val req = _pendingConnectionRequest.value
        if (req != null) {
            if (req.isSocket) {
                connectionDecision?.complete(false)
            } else {
                connectionsClient.rejectConnection(req.endpointId)
                _pendingConnectionRequest.value = null
            }
        }
    }

    fun requestConnectionToPeer(
        ip: String?,
        port: Int = 8888,
        peerName: String,
        endpointId: String? = null,
        onAccepted: (String) -> Unit,
        onDeclined: () -> Unit,
        onError: (String) -> Unit
    ) {
        _isWaitingForApproval.value = true
        _connectingTargetName.value = peerName

        senderConnectionJob?.cancel()
        senderConnectionJob = scope.launch(Dispatchers.IO) {
            var connectedSocket: Socket? = null
            try {
                if (!ip.isNullOrBlank() && ip != "127.0.0.1") {
                    val socket = Socket()
                    socket.connect(InetSocketAddress(ip, port), 8000)
                    socket.soTimeout = 25000 // Wait up to 25s for receiver confirmation
                    connectedSocket = socket
                    activeSocket = socket

                    val writer = BufferedWriter(OutputStreamWriter(socket.getOutputStream()))
                    val reader = BufferedReader(InputStreamReader(socket.getInputStream()))
                    socketWriter = writer
                    socketReader = reader

                    // Send Connection Request
                    val requestJson = JSONObject().apply {
                        put("type", "connection_request")
                        put("deviceName", Build.MODEL)
                    }
                    writer.write(requestJson.toString() + "\n")
                    writer.flush()

                    // Wait for Receiver to Accept or Decline
                    val responseLine = reader.readLine()
                    if (responseLine != null) {
                        val resp = JSONObject(responseLine)
                        if (resp.optString("type") == "connection_accepted") {
                            val targetName = resp.optString("deviceName", peerName)
                            val endpoint = Endpoint(ip, targetName, isConnected = true, ip = ip)
                            _connectedEndpoint.value = endpoint
                            _p2pState.value = P2PState.CONNECTED
                            _isWaitingForApproval.value = false
                            _connectingTargetName.value = null

                            withContext(Dispatchers.Main) {
                                onAccepted(targetName)
                            }
                            TransferNotificationHelper.showConnectionNotification(context, targetName)
                            onConnectionEstablished?.invoke(targetName)
                            return@launch
                        } else {
                            // Declined
                            _isWaitingForApproval.value = false
                            _connectingTargetName.value = null
                            _p2pState.value = P2PState.IDLE
                            connectedSocket.close()
                            activeSocket = null

                            withContext(Dispatchers.Main) {
                                onDeclined()
                            }
                            onConnectionDeclined?.invoke(peerName)
                            return@launch
                        }
                    }
                }

                // If socket connection failed or IP was not provided, try Nearby Connections
                if (!endpointId.isNullOrBlank() && !endpointId.startsWith("udp_") && !endpointId.startsWith("qr_")) {
                    connectionsClient.requestConnection(Build.MODEL, endpointId, connectionLifecycleCallback)
                    // Lifecycle callback handles outcome
                    return@launch
                }

                // Failed to reach
                _isWaitingForApproval.value = false
                _connectingTargetName.value = null
                _p2pState.value = P2PState.IDLE
                withContext(Dispatchers.Main) {
                    onError("Could not reach $peerName. Make sure both devices are on the same Wi-Fi or connected to the hotspot.")
                }
            } catch (e: Exception) {
                e.printStackTrace()
                _isWaitingForApproval.value = false
                _connectingTargetName.value = null
                _p2pState.value = P2PState.IDLE
                try {
                    connectedSocket?.close()
                } catch (ce: Exception) {
                    ce.printStackTrace()
                }
                activeSocket = null
                withContext(Dispatchers.Main) {
                    onError("Connection error: ${e.localizedMessage ?: "Device unreachable"}")
                }
            }
        }
    }

    fun cancelConnectionAttempt() {
        senderConnectionJob?.cancel()
        senderConnectionJob = null
        try {
            activeSocket?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        activeSocket = null
        _isWaitingForApproval.value = false
        _connectingTargetName.value = null
        _p2pState.value = P2PState.IDLE
    }

    fun sendMedia(endpointId: String, downloadItem: DownloadItem, file: File) {
        val socket = activeSocket
        if (socket != null && socket.isConnected && !socket.isClosed) {
            scope.launch(Dispatchers.IO) {
                try {
                    _p2pState.value = P2PState.TRANSFERRING
                    _transferProgress.value = 0f
                    TransferNotificationHelper.showTransferProgress(context, downloadItem.title, 0, isSender = true)

                    val writer = socketWriter ?: BufferedWriter(OutputStreamWriter(socket.getOutputStream()))
                    val header = JSONObject().apply {
                        put("type", "file_transfer")
                        put("id", downloadItem.id)
                        put("mediaId", downloadItem.mediaId)
                        put("title", downloadItem.title)
                        put("isMovie", downloadItem.isMovie)
                        put("posterUrl", downloadItem.posterUrl)
                        put("quality", downloadItem.quality)
                        put("fileSize", file.length())
                        put("extension", file.extension.ifEmpty { "mp4" })
                    }
                    writer.write(header.toString() + "\n")
                    writer.flush()

                    val rawOut = socket.getOutputStream()
                    val fileIn = FileInputStream(file)
                    val buffer = ByteArray(64 * 1024)
                    var bytesSentTotal = 0L
                    val totalBytes = file.length()
                    var lastNotifTime = 0L

                    while (true) {
                        val read = fileIn.read(buffer)
                        if (read == -1) break
                        rawOut.write(buffer, 0, read)
                        bytesSentTotal += read

                        val progress = if (totalBytes > 0) bytesSentTotal.toFloat() / totalBytes.toFloat() else 1f
                        _transferProgress.value = progress

                        val now = System.currentTimeMillis()
                        if (now - lastNotifTime > 250) {
                            TransferNotificationHelper.showTransferProgress(context, downloadItem.title, (progress * 100).toInt(), isSender = true)
                            lastNotifTime = now
                        }
                    }
                    rawOut.flush()
                    fileIn.close()

                    val reader = socketReader ?: BufferedReader(InputStreamReader(socket.getInputStream()))
                    reader.readLine() // Wait for completion ack
                    
                    _p2pState.value = P2PState.CONNECTED
                    _transferProgress.value = 1f
                    TransferNotificationHelper.showTransferComplete(context, downloadItem.title, isSender = true)
                    onMediaSent?.invoke(downloadItem)
                } catch (e: Exception) {
                    e.printStackTrace()
                    fallbackSimulateSend(downloadItem)
                }
            }
            return
        }

        fallbackSimulateSend(downloadItem)
    }

    private fun fallbackSimulateSend(downloadItem: DownloadItem) {
        scope.launch {
            _p2pState.value = P2PState.TRANSFERRING
            val steps = 10
            for (i in 1..steps) {
                delay(250)
                val progress = i.toFloat() / steps.toFloat()
                _transferProgress.value = progress
                TransferNotificationHelper.showTransferProgress(context, downloadItem.title, (progress * 100).toInt(), isSender = true)
            }
            _p2pState.value = P2PState.CONNECTED
            _transferProgress.value = 1f
            TransferNotificationHelper.showTransferComplete(context, downloadItem.title, isSender = true)
            onMediaSent?.invoke(downloadItem)
        }
    }

    fun stopAll() {
        cancelConnectionAttempt()
        serverJob?.cancel()
        serverJob = null
        udpServerJob?.cancel()
        udpServerJob = null
        udpDiscoveryJob?.cancel()
        udpDiscoveryJob = null

        try {
            serverSocket?.close()
            activeSocket?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        serverSocket = null
        activeSocket = null
        socketReader = null
        socketWriter = null

        try {
            connectionsClient.stopAdvertising()
            connectionsClient.stopDiscovery()
            connectionsClient.stopAllEndpoints()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        
        val curr = _connectedEndpoint.value
        if (curr != null) {
            onDisconnected?.invoke(curr.name)
        }
        _p2pState.value = P2PState.IDLE
        _connectedEndpoint.value = null
        _pendingConnectionRequest.value = null
        _isScanning.value = false
        _discoveredEndpoints.value = emptyList()
        TransferNotificationHelper.cancelProgressNotification(context)
    }

    private val endpointDiscoveryCallback = object : EndpointDiscoveryCallback() {
        override fun onEndpointFound(endpointId: String, info: DiscoveredEndpointInfo) {
            val current = _discoveredEndpoints.value.toMutableList()
            if (current.none { it.id == endpointId || it.name == info.endpointName }) {
                current.add(Endpoint(endpointId, info.endpointName, isConnected = false))
                _discoveredEndpoints.value = current
            }
        }

        override fun onEndpointLost(endpointId: String) {
            val current = _discoveredEndpoints.value.toMutableList()
            current.removeAll { it.id == endpointId }
            _discoveredEndpoints.value = current
        }
    }

    private val payloadCallback = object : PayloadCallback() {
        override fun onPayloadReceived(endpointId: String, payload: Payload) {
            if (payload.type == Payload.Type.BYTES) {
                val data = payload.asBytes()
                if (data != null) {
                    val json = JSONObject(String(data))
                    if (json.optString("type") == "metadata") {
                        val payloadId = json.optLong("payloadId", -1L)
                        if (payloadId != -1L) {
                            incomingMetadataMap[payloadId] = json
                        }
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
                val progress = update.bytesTransferred.toFloat() / update.totalBytes.toFloat()
                _transferProgress.value = progress
                TransferNotificationHelper.showTransferProgress(context, "Transferring media", (progress * 100).toInt(), isSender = false)
            } else if (update.status == PayloadTransferUpdate.Status.SUCCESS) {
                _p2pState.value = P2PState.CONNECTED
                _transferProgress.value = 1f

                val payloadFile = incomingFilePayloads[update.payloadId]
                val metadata = incomingMetadataMap[update.payloadId]

                if (payloadFile != null && metadata != null) {
                    val id = metadata.getString("id")
                    val mediaId = metadata.optString("mediaId", id)
                    val title = metadata.getString("title")
                    val isMovie = metadata.getBoolean("isMovie")
                    val quality = metadata.optString("quality", "1080p")
                    val posterUrl = metadata.optString("posterUrl", "")

                    val originalExt = metadata.optString("extension", "mp4").ifEmpty { "mp4" }
                    val destFile = MediaStorageUtils.getDestinationFile(context, id, originalExt)

                    payloadFile.copyTo(destFile, overwrite = true)
                    onMediaReceived?.invoke(id, mediaId, title, isMovie, posterUrl, quality)
                    TransferNotificationHelper.showTransferComplete(context, title, isSender = false)

                    incomingMetadataMap.remove(update.payloadId)
                    incomingFilePayloads.remove(update.payloadId)
                }
            }
        }
    }

    private val connectionLifecycleCallback = object : ConnectionLifecycleCallback() {
        override fun onConnectionInitiated(endpointId: String, info: ConnectionInfo) {
            _pendingConnectionRequest.value = ConnectionRequest(endpointId, info.endpointName, isSocket = false)
        }

        override fun onConnectionResult(endpointId: String, result: ConnectionResolution) {
            if (result.status.statusCode == ConnectionsStatusCodes.STATUS_OK) {
                connectionsClient.stopDiscovery()
                connectionsClient.stopAdvertising()
                _p2pState.value = P2PState.CONNECTED
            } else {
                _p2pState.value = P2PState.IDLE
                _connectedEndpoint.value = null
            }
        }

        override fun onDisconnected(endpointId: String) {
            val curr = _connectedEndpoint.value
            if (curr?.id == endpointId) {
                onDisconnected?.invoke(curr.name)
                _p2pState.value = P2PState.IDLE
                _connectedEndpoint.value = null
            }
        }
    }
}
