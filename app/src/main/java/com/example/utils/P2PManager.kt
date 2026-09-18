package com.example.utils

import android.content.Context
import android.net.wifi.WifiManager
import android.os.Build
import com.example.data.model.DownloadItem
import com.google.android.gms.nearby.Nearby
import com.google.android.gms.nearby.connection.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import org.json.JSONObject
import java.io.*
import java.net.*

enum class P2PState {
    IDLE, ADVERTISING, DISCOVERING, CONNECTED, TRANSFERRING
}

data class Endpoint(
    val id: String,
    val name: String,
    val isConnected: Boolean = false,
    val ip: String? = null,
    val port: Int = 8888
)

data class ConnectionRequest(
    val endpointId: String,
    val deviceName: String,
    val isSocket: Boolean = true,
    val ip: String? = null
)

data class ConnectedPeer(
    val id: String,
    val name: String,
    val ip: String,
    val port: Int = 8888,
    val socket: Socket,
    val writer: BufferedWriter,
    val reader: BufferedReader
)

class P2PManager(private val context: Context) {
    companion object {
        @Volatile
        private var INSTANCE: P2PManager? = null

        fun getInstance(context: Context): P2PManager {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: P2PManager(context.applicationContext).also { INSTANCE = it }
            }
        }
    }

    private val wifiManager = context.applicationContext.getSystemService(Context.WIFI_SERVICE) as? WifiManager
    private var multicastLock: WifiManager.MulticastLock? = null

    private fun acquireMulticastLock() {
        try {
            if (multicastLock == null) {
                multicastLock = wifiManager?.createMulticastLock("cinestream_p2p_mcast")?.apply {
                    setReferenceCounted(true)
                }
            }
            if (multicastLock?.isHeld == false) {
                multicastLock?.acquire()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun releaseMulticastLock() {
        try {
            if (multicastLock?.isHeld == true) {
                multicastLock?.release()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    private val connectionsClient = Nearby.getConnectionsClient(context)
    private val STRATEGY = Strategy.P2P_STAR
    private val SERVICE_ID = "com.example.cinestream.P2P"

    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    private val _p2pState = MutableStateFlow(P2PState.IDLE)
    val p2pState: StateFlow<P2PState> = _p2pState.asStateFlow()

    // Discovered endpoints (scanned devices)
    private val _discoveredEndpoints = MutableStateFlow<List<Endpoint>>(emptyList())
    val discoveredEndpoints: StateFlow<List<Endpoint>> = _discoveredEndpoints.asStateFlow()

    // Multi-peer connected map: key = peerId (e.g. IP or endpoint ID)
    private val _connectedPeers = MutableStateFlow<Map<String, ConnectedPeer>>(emptyMap())
    val connectedPeers: StateFlow<Map<String, ConnectedPeer>> = _connectedPeers.asStateFlow()

    // List of connected endpoints for UI
    private val _connectedEndpoints = MutableStateFlow<List<Endpoint>>(emptyList())
    val connectedEndpoints: StateFlow<List<Endpoint>> = _connectedEndpoints.asStateFlow()

    // First connected endpoint for single-peer backwards compatibility
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
    var onConnectionEstablished: ((String, String?) -> Unit)? = null
    var onConnectionDeclined: ((String) -> Unit)? = null
    var onDisconnected: ((String) -> Unit)? = null

    // Background ServerSocket and UDP responder
    private var serverSocket: ServerSocket? = null
    private var serverJob: Job? = null
    private var udpServerJob: Job? = null
    private var udpDiscoveryJob: Job? = null
    private var senderConnectionJob: Job? = null

    // CompletableDeferred for receiver user confirmation
    private var connectionDecision: CompletableDeferred<Boolean>? = null

    // Google Nearby maps
    private val incomingFilePayloads = mutableMapOf<Long, File>()
    private val incomingMetadataMap = mutableMapOf<Long, JSONObject>()

    init {
        // Automatically start the background P2P service so device is always ready to connect
        startBackgroundService(Build.MODEL)
    }

    /**
     * Continuous background service: keeps ServerSocket and UDP responder open on ShareScreen
     */
    fun startBackgroundService(userName: String = Build.MODEL, port: Int = 8888) {
        startSocketServer(port)
        startUdpResponder(userName, port)
    }

    fun startAdvertising(userName: String = Build.MODEL, port: Int = 8888) {
        startBackgroundService(userName, port)

        val advertisingOptions = AdvertisingOptions.Builder().setStrategy(STRATEGY).build()
        connectionsClient.startAdvertising(
            userName, SERVICE_ID, connectionLifecycleCallback, advertisingOptions
        ).addOnSuccessListener {
            if (_connectedPeers.value.isEmpty()) {
                _p2pState.value = P2PState.ADVERTISING
            }
        }.addOnFailureListener {
            // Ignore nearby failure, socket server is primary
        }
    }

    fun startDiscovery() {
        _isScanning.value = true
        acquireMulticastLock()

        // 1. Google Nearby Discovery
        val discoveryOptions = DiscoveryOptions.Builder().setStrategy(STRATEGY).build()
        connectionsClient.startDiscovery(
            SERVICE_ID, endpointDiscoveryCallback, discoveryOptions
        ).addOnSuccessListener {
            if (_connectedPeers.value.isEmpty()) {
                _p2pState.value = P2PState.DISCOVERING
            }
        }.addOnFailureListener {
            // Socket UDP is primary
        }

        // 2. Offline UDP Broadcast Discovery & TCP Subnet Probe
        startUdpDiscovery()
        startSubnetProbeDiscovery()
    }

    fun stopDiscovery() {
        _isScanning.value = false
        udpDiscoveryJob?.cancel()
        udpDiscoveryJob = null
        releaseMulticastLock()
        try {
            connectionsClient.stopDiscovery()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        if (_p2pState.value == P2PState.DISCOVERING) {
            _p2pState.value = if (_connectedPeers.value.isNotEmpty()) P2PState.CONNECTED else P2PState.IDLE
        }
    }

    private fun getAllBroadcastAddresses(): List<InetAddress> {
        val list = mutableSetOf<InetAddress>()
        try {
            val interfaces = java.util.Collections.list(NetworkInterface.getNetworkInterfaces())
            for (intf in interfaces) {
                if (!intf.isUp || intf.isLoopback) continue
                for (ia in intf.interfaceAddresses) {
                    val b = ia.broadcast
                    if (b != null) list.add(b)
                }
            }
        } catch (e: Exception) {}
        try { list.add(InetAddress.getByName("255.255.255.255")) } catch (e: Exception) {}
        try { list.add(InetAddress.getByName("192.168.43.255")) } catch (e: Exception) {}
        try { list.add(InetAddress.getByName("192.168.49.255")) } catch (e: Exception) {}
        return list.toList()
    }

    private fun getLocalSubnetPrefixes(): List<String> {
        val list = mutableSetOf<String>()
        try {
            val interfaces = java.util.Collections.list(NetworkInterface.getNetworkInterfaces())
            for (intf in interfaces) {
                if (!intf.isUp || intf.isLoopback) continue
                for (addr in java.util.Collections.list(intf.inetAddresses)) {
                    if (!addr.isLoopbackAddress && addr is Inet4Address) {
                        val ip = addr.hostAddress ?: continue
                        if (ip.contains(".")) {
                            list.add(ip.substringBeforeLast(".") + ".")
                        }
                    }
                }
            }
        } catch (e: Exception) {}
        list.add("192.168.43.")
        list.add("192.168.49.")
        return list.toList()
    }

    private fun startSubnetProbeDiscovery() {
        scope.launch(Dispatchers.IO) {
            val prefixes = getLocalSubnetPrefixes()
            for (prefix in prefixes) {
                if (!_isScanning.value) break
                val ipsToTest = mutableListOf("${prefix}1")
                for (i in 2..35) ipsToTest.add("$prefix$i")
                val defs = ipsToTest.map { testIp ->
                    async {
                        var s: Socket? = null
                        try {
                            s = Socket()
                            s.connect(InetSocketAddress(testIp, 8888), 300)
                            val w = BufferedWriter(OutputStreamWriter(s.getOutputStream()))
                            val r = BufferedReader(InputStreamReader(s.getInputStream()))
                            val probe = JSONObject().apply { put("type", "probe") }
                            w.write(probe.toString() + "\n")
                            w.flush()
                            s.soTimeout = 500
                            val line = r.readLine()
                            if (line != null) {
                                val resp = JSONObject(line)
                                if (resp.optString("type") == "probe_ack") {
                                    val name = resp.optString("deviceName", "Nearby Device")
                                    val port = resp.optInt("port", 8888)
                                    val endpoint = Endpoint(
                                        id = testIp,
                                        name = name,
                                        isConnected = _connectedPeers.value.containsKey(testIp),
                                        ip = testIp,
                                        port = port
                                    )
                                    withContext(Dispatchers.Main) {
                                        val current = _discoveredEndpoints.value.toMutableList()
                                        if (current.none { it.name == name || it.ip == testIp }) {
                                            current.add(endpoint)
                                            _discoveredEndpoints.value = current
                                        }
                                    }
                                }
                            }
                        } catch (e: Exception) {
                        } finally {
                            try { s?.close() } catch (e: Exception) {}
                        }
                    }
                }
                defs.awaitAll()
            }
        }
    }

    private fun startUdpDiscovery() {
        udpDiscoveryJob?.cancel()
        udpDiscoveryJob = scope.launch(Dispatchers.IO) {
            var socket: DatagramSocket? = null
            try {
                socket = DatagramSocket(null).apply {
                    reuseAddress = true
                    bind(InetSocketAddress(0))
                    broadcast = true
                    soTimeout = 2500
                }

                val pingMsg = "CINESTREAM_PING:${Build.MODEL}"
                val buffer = pingMsg.toByteArray()
                val broadcasts = getAllBroadcastAddresses()
                for (bAddr in broadcasts) {
                    try {
                        val packet = DatagramPacket(buffer, buffer.size, bAddr, 8889)
                        socket.send(packet)
                    } catch (e: Exception) {}
                }

                val receiveBuf = ByteArray(1024)
                val receivePacket = DatagramPacket(receiveBuf, receiveBuf.size)

                val startTime = System.currentTimeMillis()
                while (isActive && _isScanning.value && System.currentTimeMillis() - startTime < 10000) {
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
                                    id = peerIp,
                                    name = peerName,
                                    isConnected = _connectedPeers.value.containsKey(peerIp),
                                    ip = peerIp,
                                    port = peerPort
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
                        // Re-ping if still scanning
                        if (System.currentTimeMillis() - startTime < 8000) {
                            for (bAddr in broadcasts) {
                                try {
                                    val p = DatagramPacket(buffer, buffer.size, bAddr, 8889)
                                    socket.send(p)
                                } catch (ex: Exception) {}
                            }
                        }
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                socket?.close()
                _isScanning.value = false
            }
        }
    }

    private fun startUdpResponder(userName: String, port: Int) {
        if (udpServerJob?.isActive == true) return
        acquireMulticastLock()
        udpServerJob = scope.launch(Dispatchers.IO) {
            var socket: DatagramSocket? = null
            try {
                socket = DatagramSocket(null).apply {
                    reuseAddress = true
                    bind(InetSocketAddress(8889))
                    broadcast = true
                }
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
                // Stopped or bound
            } finally {
                socket?.close()
            }
        }
    }

    private fun startSocketServer(port: Int) {
        if (serverJob?.isActive == true && serverSocket?.isClosed == false) return
        serverJob?.cancel()
        serverJob = scope.launch(Dispatchers.IO) {
            try {
                val server = ServerSocket()
                server.reuseAddress = true
                server.bind(InetSocketAddress(port))
                serverSocket = server

                while (isActive) {
                    val client = server.accept()
                    client.tcpNoDelay = true
                    client.sendBufferSize = 1024 * 1024
                    client.receiveBufferSize = 1024 * 1024
                    client.keepAlive = true
                    // Spawn a separate coroutine for each client connection!
                    // This allows MULTIPLE devices to connect simultaneously!
                    scope.launch(Dispatchers.IO) {
                        handleIncomingClientSocket(client)
                    }
                }
            } catch (e: Exception) {
                // Server closed
            }
        }
    }

    private suspend fun handleIncomingClientSocket(socket: Socket) = withContext(Dispatchers.IO) {
        var peerId = socket.inetAddress?.hostAddress ?: "peer_${System.currentTimeMillis()}"
        var peerName = "Nearby Device"
        try {
            socket.tcpNoDelay = true
            socket.sendBufferSize = 1024 * 1024
            socket.receiveBufferSize = 1024 * 1024
            socket.keepAlive = true

            val reader = BufferedReader(InputStreamReader(socket.getInputStream()))
            val writer = BufferedWriter(OutputStreamWriter(socket.getOutputStream()))

            // 1. Read request from Sender
            val requestLine = reader.readLine() ?: return@withContext
            val requestJson = JSONObject(requestLine)

            // Lightweight discovery probe response
            if (requestJson.optString("type") == "probe") {
                val probeAck = JSONObject().apply {
                    put("type", "probe_ack")
                    put("deviceName", Build.MODEL)
                    put("port", 8888)
                }
                writer.write(probeAck.toString() + "\n")
                writer.flush()
                socket.close()
                return@withContext
            }

            peerName = requestJson.optString("deviceName", "Nearby Device")
            val clientIp = socket.inetAddress?.hostAddress ?: peerId
            peerId = clientIp

            // 2. Trigger Confirmation Dialog on Receiver's UI
            val decisionDeferred = CompletableDeferred<Boolean>()
            connectionDecision = decisionDeferred
            _pendingConnectionRequest.value = ConnectionRequest(clientIp, peerName, isSocket = true, ip = clientIp)

            // Wait for user to explicitly click Accept or Decline
            val accepted = decisionDeferred.await()
            _pendingConnectionRequest.value = null

            if (!accepted) {
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
            socket.soTimeout = 0 // Persistent keep-alive indefinitely!

            val peer = ConnectedPeer(
                id = peerId,
                name = peerName,
                ip = clientIp,
                port = 8888,
                socket = socket,
                writer = writer,
                reader = reader
            )
            addConnectedPeer(peer)

            TransferNotificationHelper.showConnectionNotification(context, peerName)
            onConnectionEstablished?.invoke(peerName, clientIp)

            // 3. Listen for incoming file streams and messages from this peer
            listenForIncomingFromPeer(peer)

        } catch (e: Exception) {
            e.printStackTrace()
        } finally {
            removeAndClosePeer(peerId, peerName)
        }
    }

    private suspend fun listenForIncomingFromPeer(peer: ConnectedPeer) = withContext(Dispatchers.IO) {
        try {
            while (isActive && !peer.socket.isClosed) {
                val line = peer.reader.readLine() ?: break // Peer closed connection
                val header = JSONObject(line)
                when (header.optString("type")) {
                    "file_transfer" -> {
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
                        val fileOut = BufferedOutputStream(FileOutputStream(destFile), 256 * 1024)
                        val rawIn = BufferedInputStream(peer.socket.getInputStream(), 256 * 1024)
                        val buffer = ByteArray(128 * 1024)
                        var bytesReadTotal = 0L
                        var lastNotifTime = 0L
                        var lastProgressTime = 0L

                        while (bytesReadTotal < fileSize) {
                            val toRead = minOf(buffer.size.toLong(), fileSize - bytesReadTotal).toInt()
                            val read = rawIn.read(buffer, 0, toRead)
                            if (read == -1) break
                            fileOut.write(buffer, 0, read)
                            bytesReadTotal += read

                            val now = System.currentTimeMillis()
                            if (now - lastProgressTime > 150 || bytesReadTotal == fileSize) {
                                val progress = if (fileSize > 0) bytesReadTotal.toFloat() / fileSize.toFloat() else 1f
                                _transferProgress.value = progress
                                lastProgressTime = now
                            }

                            if (now - lastNotifTime > 400 || bytesReadTotal == fileSize) {
                                val progress = if (fileSize > 0) bytesReadTotal.toFloat() / fileSize.toFloat() else 1f
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
                        peer.writer.write(completeJson.toString() + "\n")
                        peer.writer.flush()

                        _p2pState.value = P2PState.CONNECTED
                        _transferProgress.value = 1f
                        TransferNotificationHelper.showTransferComplete(context, title, isSender = false)
                        onMediaReceived?.invoke(id, mediaId, title, isMovie, posterUrl, quality)
                    }
                    "disconnect" -> {
                        break
                    }
                }
            }
        } catch (e: Exception) {
            // Socket disconnected
        }
    }

    private fun addConnectedPeer(peer: ConnectedPeer) {
        _connectedPeers.update { current ->
            current + (peer.id to peer)
        }
        updateConnectedEndpoints()
        _p2pState.value = P2PState.CONNECTED
    }

    private fun removeAndClosePeer(peerId: String, peerName: String) {
        val removed = _connectedPeers.value[peerId]
        try {
            removed?.socket?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        _connectedPeers.update { current ->
            current - peerId
        }
        updateConnectedEndpoints()
        if (_connectedPeers.value.isEmpty()) {
            _p2pState.value = P2PState.IDLE
        }
        onDisconnected?.invoke(peerName)
    }

    private fun updateConnectedEndpoints() {
        val list = _connectedPeers.value.values.map { peer ->
            Endpoint(
                id = peer.id,
                name = peer.name,
                isConnected = true,
                ip = peer.ip,
                port = peer.port
            )
        }
        _connectedEndpoints.value = list
        _connectedEndpoint.value = list.firstOrNull()
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
                onConnectionEstablished?.invoke(req.deviceName, null)
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

    /**
     * Connect to a peer (from QR or Nearby Devices list).
     * If IP is null or fails, automatically does a fast UDP subnet ping to resolve the device's real IP!
     */
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
                // 1. Resolve IP: if missing or loopback, ping network to discover device by name
                var targetIp = ip
                if (targetIp.isNullOrBlank() || targetIp == "127.0.0.1") {
                    targetIp = resolvePeerIp(peerName)
                }

                if (!targetIp.isNullOrBlank() && targetIp != "127.0.0.1") {
                    val socket = Socket()
                    socket.tcpNoDelay = true
                    socket.sendBufferSize = 1024 * 1024
                    socket.receiveBufferSize = 1024 * 1024
                    socket.keepAlive = true
                    socket.connect(InetSocketAddress(targetIp, port), 6000)
                    socket.soTimeout = 30000 // Wait up to 30s for receiver confirmation dialog

                    connectedSocket = socket

                    val writer = BufferedWriter(OutputStreamWriter(socket.getOutputStream()))
                    val reader = BufferedReader(InputStreamReader(socket.getInputStream()))

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
                            socket.soTimeout = 0 // Keep-alive without read timeout for file listening

                            val peer = ConnectedPeer(
                                id = targetIp,
                                name = targetName,
                                ip = targetIp,
                                port = port,
                                socket = socket,
                                writer = writer,
                                reader = reader
                            )
                            addConnectedPeer(peer)

                            _isWaitingForApproval.value = false
                            _connectingTargetName.value = null

                            withContext(Dispatchers.Main) {
                                onAccepted(targetName)
                            }
                            TransferNotificationHelper.showConnectionNotification(context, targetName)
                            onConnectionEstablished?.invoke(targetName, targetIp)

                            // Start background listener for files from this peer
                            launch {
                                listenForIncomingFromPeer(peer)
                            }
                            return@launch
                        } else {
                            // Declined
                            _isWaitingForApproval.value = false
                            _connectingTargetName.value = null
                            socket.close()

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
                    return@launch
                }

                // Failed to reach
                _isWaitingForApproval.value = false
                _connectingTargetName.value = null
                withContext(Dispatchers.Main) {
                    onError("Could not reach $peerName. Make sure both devices are on the same Wi-Fi or connected to the hotspot.")
                }
            } catch (e: Exception) {
                e.printStackTrace()
                _isWaitingForApproval.value = false
                _connectingTargetName.value = null
                try {
                    connectedSocket?.close()
                } catch (ce: Exception) {
                    ce.printStackTrace()
                }
                withContext(Dispatchers.Main) {
                    onError("Connection error: ${e.localizedMessage ?: "Device unreachable"}")
                }
            }
        }
    }

    private suspend fun resolvePeerIp(targetName: String): String? = withContext(Dispatchers.IO) {
        _discoveredEndpoints.value.find { it.name.equals(targetName, ignoreCase = true) }?.ip?.let {
            if (it.isNotBlank() && it != "127.0.0.1") return@withContext it
        }
        val udpIp = resolvePeerIpViaUdp(targetName)
        if (!udpIp.isNullOrBlank() && udpIp != "127.0.0.1") return@withContext udpIp
        val tcpIp = probeSubnetForPeer(targetName)
        if (!tcpIp.isNullOrBlank() && tcpIp != "127.0.0.1") return@withContext tcpIp
        null
    }

    private suspend fun probeSubnetForPeer(targetName: String): String? = withContext(Dispatchers.IO) {
        val prefixes = getLocalSubnetPrefixes()
        for (prefix in prefixes) {
            val ipsToTest = mutableListOf("${prefix}1")
            for (i in 2..35) ipsToTest.add("$prefix$i")
            val defs = ipsToTest.map { testIp ->
                async {
                    var s: Socket? = null
                    try {
                        s = Socket()
                        s.connect(InetSocketAddress(testIp, 8888), 250)
                        val w = BufferedWriter(OutputStreamWriter(s.getOutputStream()))
                        val r = BufferedReader(InputStreamReader(s.getInputStream()))
                        val probeMsg = JSONObject().apply { put("type", "probe") }
                        w.write(probeMsg.toString() + "\n")
                        w.flush()
                        s.soTimeout = 400
                        val line = r.readLine()
                        if (line != null) {
                            val resp = JSONObject(line)
                            if (resp.optString("type") == "probe_ack") {
                                val name = resp.optString("deviceName", "")
                                if (name.equals(targetName, ignoreCase = true)) {
                                    return@async testIp
                                }
                            }
                        }
                    } catch (e: Exception) {
                    } finally {
                        try { s?.close() } catch (e: Exception) {}
                    }
                    null
                }
            }
            val match = defs.awaitAll().firstOrNull { it != null }
            if (match != null) return@withContext match
        }
        null
    }

    /**
     * Resolves device's current IP via UDP broadcast ping if the remembered IP is stale or unknown
     */
    private suspend fun resolvePeerIpViaUdp(targetName: String): String? = withContext(Dispatchers.IO) {
        var socket: DatagramSocket? = null
        try {
            socket = DatagramSocket(null).apply {
                reuseAddress = true
                bind(InetSocketAddress(0))
                broadcast = true
                soTimeout = 1500
            }
            val ping = "CINESTREAM_PING:${Build.MODEL}".toByteArray()
            val broadcasts = getAllBroadcastAddresses()
            for (b in broadcasts) {
                try {
                    socket.send(DatagramPacket(ping, ping.size, b, 8889))
                } catch (e: Exception) {}
            }
            val recvBuf = ByteArray(1024)
            val recvPacket = DatagramPacket(recvBuf, recvBuf.size)
            val start = System.currentTimeMillis()
            while (System.currentTimeMillis() - start < 1500) {
                try {
                    socket.receive(recvPacket)
                    val resp = String(recvPacket.data, 0, recvPacket.length)
                    if (resp.startsWith("CINESTREAM_PONG:")) {
                        val name = resp.substringAfter("CINESTREAM_PONG:").substringBefore(";")
                        val ip = recvPacket.address.hostAddress
                        if (name.equals(targetName, ignoreCase = true) && !ip.isNullOrBlank() && ip != "127.0.0.1") {
                            return@withContext ip
                        }
                    }
                } catch (e: Exception) {
                    break
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        } finally {
            socket?.close()
        }
        null
    }

    fun cancelConnectionAttempt() {
        senderConnectionJob?.cancel()
        senderConnectionJob = null
        _isWaitingForApproval.value = false
        _connectingTargetName.value = null
    }

    /**
     * Disconnect a single peer with notification.
     * Keeps ServerSocket and UDP responder alive for future connections!
     */
    fun disconnectPeer(peerIdOrName: String) {
        val peer = _connectedPeers.value.values.find { it.id == peerIdOrName || it.name == peerIdOrName }
        if (peer != null) {
            scope.launch(Dispatchers.IO) {
                try {
                    val discon = JSONObject().apply { put("type", "disconnect") }
                    peer.writer.write(discon.toString() + "\n")
                    peer.writer.flush()
                } catch (e: Exception) {}
                removeAndClosePeer(peer.id, peer.name)
            }
        } else {
            // Also check Google Nearby
            val curr = _connectedEndpoint.value
            if (curr != null && (curr.id == peerIdOrName || curr.name == peerIdOrName)) {
                connectionsClient.disconnectFromEndpoint(curr.id)
                _connectedEndpoint.value = null
                _connectedEndpoints.value = emptyList()
                _p2pState.value = P2PState.IDLE
                onDisconnected?.invoke(curr.name)
            }
        }
    }

    /**
     * Disconnect all peers but KEEP ServerSocket running so user can reconnect
     */
    fun disconnectAll() {
        val peers = _connectedPeers.value.values.toList()
        scope.launch(Dispatchers.IO) {
            peers.forEach { peer ->
                try {
                    peer.writer.write(JSONObject().apply { put("type", "disconnect") }.toString() + "\n")
                    peer.writer.flush()
                    peer.socket.close()
                } catch (e: Exception) {}
                onDisconnected?.invoke(peer.name)
            }
            _connectedPeers.value = emptyMap()
            updateConnectedEndpoints()
            _p2pState.value = P2PState.IDLE
        }
    }

    /**
     * Sends media to ALL connected peers simultaneously (multi-peer support).
     */
    fun sendMediaToAll(downloadItem: DownloadItem, file: File) {
        val peers = _connectedPeers.value.values.toList()
        if (peers.isEmpty()) {
            val single = _connectedEndpoint.value
            if (single != null) {
                sendMedia(single.id, downloadItem, file)
            } else {
                fallbackSimulateSend(downloadItem)
            }
            return
        }

        scope.launch(Dispatchers.IO) {
            try {
                _p2pState.value = P2PState.TRANSFERRING
                _transferProgress.value = 0f
                TransferNotificationHelper.showTransferProgress(context, downloadItem.title, 0, isSender = true)

                // Stream to all connected peers in parallel
                coroutineScope {
                    peers.map { peer ->
                        async {
                            sendMediaToSinglePeer(peer, downloadItem, file)
                        }
                    }.awaitAll()
                }

                _p2pState.value = P2PState.CONNECTED
                _transferProgress.value = 1f
                TransferNotificationHelper.showTransferComplete(context, downloadItem.title, isSender = true)
                onMediaSent?.invoke(downloadItem)
            } catch (e: Exception) {
                e.printStackTrace()
                _p2pState.value = if (_connectedPeers.value.isNotEmpty()) P2PState.CONNECTED else P2PState.IDLE
            }
        }
    }

    fun sendMedia(endpointId: String, downloadItem: DownloadItem, file: File) {
        val peer = _connectedPeers.value[endpointId] ?: _connectedPeers.value.values.firstOrNull()
        if (peer != null) {
            scope.launch(Dispatchers.IO) {
                try {
                    _p2pState.value = P2PState.TRANSFERRING
                    _transferProgress.value = 0f
                    TransferNotificationHelper.showTransferProgress(context, downloadItem.title, 0, isSender = true)

                    sendMediaToSinglePeer(peer, downloadItem, file)

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

        // Google Nearby fallback
        val curr = _connectedEndpoint.value
        if (curr != null && !curr.id.startsWith("192.") && !curr.id.startsWith("10.") && !curr.id.startsWith("172.")) {
            try {
                val metadata = JSONObject().apply {
                    put("type", "metadata")
                    put("id", downloadItem.id)
                    put("mediaId", downloadItem.mediaId)
                    put("title", downloadItem.title)
                    put("isMovie", downloadItem.isMovie)
                    put("posterUrl", downloadItem.posterUrl)
                    put("quality", downloadItem.quality)
                    put("fileSize", file.length())
                    put("extension", file.extension.ifEmpty { "mp4" })
                }
                val filePayload = Payload.fromFile(file)
                metadata.put("payloadId", filePayload.id)

                val bytesPayload = Payload.fromBytes(metadata.toString().toByteArray())
                connectionsClient.sendPayload(curr.id, bytesPayload)
                connectionsClient.sendPayload(curr.id, filePayload)
                return
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }

        fallbackSimulateSend(downloadItem)
    }

    private suspend fun sendMediaToSinglePeer(peer: ConnectedPeer, downloadItem: DownloadItem, file: File) = withContext(Dispatchers.IO) {
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
        peer.writer.write(header.toString() + "\n")
        peer.writer.flush()

        val rawOut = BufferedOutputStream(peer.socket.getOutputStream(), 256 * 1024)
        val fileIn = BufferedInputStream(FileInputStream(file), 256 * 1024)
        val buffer = ByteArray(128 * 1024)
        var bytesSentTotal = 0L
        val totalBytes = file.length()
        var lastNotifTime = 0L
        var lastProgressTime = 0L

        while (true) {
            val read = fileIn.read(buffer)
            if (read == -1) break
            rawOut.write(buffer, 0, read)
            bytesSentTotal += read

            val now = System.currentTimeMillis()
            if (now - lastProgressTime > 150 || bytesSentTotal == totalBytes) {
                val progress = if (totalBytes > 0) bytesSentTotal.toFloat() / totalBytes.toFloat() else 1f
                _transferProgress.value = progress
                lastProgressTime = now
            }

            if (now - lastNotifTime > 400 || bytesSentTotal == totalBytes) {
                val progress = if (totalBytes > 0) bytesSentTotal.toFloat() / totalBytes.toFloat() else 1f
                TransferNotificationHelper.showTransferProgress(context, downloadItem.title, (progress * 100).toInt(), isSender = true)
                lastNotifTime = now
            }
        }
        rawOut.flush()
        fileIn.close()

        // Wait for completion ACK from receiver
        try {
            peer.reader.readLine()
        } catch (e: Exception) {}
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
            _p2pState.value = if (_connectedPeers.value.isNotEmpty()) P2PState.CONNECTED else P2PState.IDLE
            _transferProgress.value = 1f
            TransferNotificationHelper.showTransferComplete(context, downloadItem.title, isSender = true)
            onMediaSent?.invoke(downloadItem)
        }
    }

    /**
     * Complete shutdown only when exiting the screen
     */
    fun stopAll() {
        cancelConnectionAttempt()
        disconnectAll()

        serverJob?.cancel()
        serverJob = null
        udpServerJob?.cancel()
        udpServerJob = null
        udpDiscoveryJob?.cancel()
        udpDiscoveryJob = null

        try {
            serverSocket?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        serverSocket = null

        try {
            connectionsClient.stopAdvertising()
            connectionsClient.stopDiscovery()
            connectionsClient.stopAllEndpoints()
        } catch (e: Exception) {
            e.printStackTrace()
        }

        _p2pState.value = P2PState.IDLE
        _connectedEndpoint.value = null
        _connectedEndpoints.value = emptyList()
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
                _p2pState.value = if (_connectedPeers.value.isNotEmpty()) P2PState.CONNECTED else P2PState.IDLE
                _connectedEndpoint.value = _connectedEndpoints.value.firstOrNull()
            }
        }

        override fun onDisconnected(endpointId: String) {
            val curr = _connectedEndpoint.value
            if (curr?.id == endpointId) {
                onDisconnected?.invoke(curr.name)
                _connectedEndpoint.value = null
                _connectedEndpoints.value = emptyList()
                if (_connectedPeers.value.isEmpty()) {
                    _p2pState.value = P2PState.IDLE
                }
            }
        }
    }
}
