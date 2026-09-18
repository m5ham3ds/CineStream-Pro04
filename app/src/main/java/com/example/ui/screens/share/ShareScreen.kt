package com.example.ui.screens.share

import androidx.compose.ui.res.stringResource
import com.example.ui.theme.SuccessGreen
import com.example.R

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.net.Uri
import android.os.Build
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.Folder
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Movie
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Tv
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import coil.compose.AsyncImage
import com.example.data.model.DownloadItem
import com.example.data.model.P2PTransferRecord
import com.example.data.repository.DownloadRepository
import com.example.data.repository.NearbyDevice
import com.example.data.repository.NearbyDeviceRepository
import com.example.data.repository.P2PTransferRepository
import com.example.ui.components.QrCodeScannerDialog
import com.example.utils.HotspotManager
import com.example.utils.MediaStorageUtils
import com.example.utils.NetworkUtils
import com.example.utils.P2PManager
import com.example.utils.P2PState
import com.example.utils.QRCodeGenerator
import com.google.accompanist.permissions.ExperimentalPermissionsApi
import com.google.accompanist.permissions.rememberMultiplePermissionsState
import kotlinx.coroutines.launch
import java.io.File

@OptIn(ExperimentalPermissionsApi::class, ExperimentalMaterial3Api::class)
@Composable
fun ShareScreen(
    onBack: () -> Unit,
    onItemClick: (String, Boolean) -> Unit = { _, _ -> }
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val p2pManager = remember { P2PManager(context) }
    val hotspotManager = remember { HotspotManager(context) }
    val downloadRepository = remember { DownloadRepository(context) }
    val p2pTransferRepository = remember { P2PTransferRepository(context) }
    val nearbyDeviceRepository = remember { NearbyDeviceRepository(context) }
    
    val p2pState by p2pManager.p2pState.collectAsState()
    val connectedEndpoint by p2pManager.connectedEndpoint.collectAsState()
    val connectedEndpoints by p2pManager.connectedEndpoints.collectAsState()
    val discoveredEndpoints by p2pManager.discoveredEndpoints.collectAsState()
    val transferProgress by p2pManager.transferProgress.collectAsState()
    val pendingConnectionRequest by p2pManager.pendingConnectionRequest.collectAsState()
    val isWaitingForApproval by p2pManager.isWaitingForApproval.collectAsState()
    val connectingTargetName by p2pManager.connectingTargetName.collectAsState()
    val isScanning by p2pManager.isScanning.collectAsState()
    val rememberedDevices by nearbyDeviceRepository.devices.collectAsState()
    
    val allDownloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val completedDownloads = remember(allDownloads) { allDownloads.filter { it.isCompleted } }
    val recentTransfers by p2pTransferRepository.transfers.collectAsState()

    var showSendDialog by remember { mutableStateOf(false) }
    var showReceiveDialog by remember { mutableStateOf(false) }
    var showQrScannerDialog by remember { mutableStateOf(false) }
    var showHowItWorksDialog by remember { mutableStateOf(false) }
    var deviceToDisconnect by remember { mutableStateOf<NearbyDevice?>(null) }
    var qrBitmap by remember { mutableStateOf<Bitmap?>(null) }
    var selectedContentType by remember { mutableStateOf("Movies") }

    // Sync callbacks with repositories
    DisposableEffect(Unit) {
        // Start background socket server and UDP responder so device is always discoverable and ready to reconnect
        p2pManager.startBackgroundService(Build.MODEL, 8888)

        p2pManager.onConnectionEstablished = { peerName, peerIp ->
            nearbyDeviceRepository.addOrUpdateDevice(
                NearbyDevice(
                    id = peerIp ?: peerName,
                    name = peerName,
                    ip = peerIp,
                    port = 8888,
                    isConnected = true,
                    lastSeen = System.currentTimeMillis()
                )
            )
        }
        
        p2pManager.onDisconnected = { peerName ->
            nearbyDeviceRepository.setDeviceConnected(peerName, false)
        }
        
        p2pManager.onConnectionDeclined = { peerName ->
            Toast.makeText(context, "Connection declined by $peerName", Toast.LENGTH_SHORT).show()
            nearbyDeviceRepository.setDeviceConnected(peerName, false)
        }

        p2pManager.onMediaReceived = { id, mediaId, title, isMovie, posterUrl, quality ->
            scope.launch {
                downloadRepository.addCompletedDownload(
                    DownloadItem(
                        id = id, mediaId = mediaId,
                        title = title,
                        posterUrl = posterUrl,
                        isMovie = isMovie,
                        quality = quality,
                        progress = 1f,
                        isCompleted = true
                    )
                )
                p2pTransferRepository.recordTransfer(
                    P2PTransferRecord(
                        id = id,
                        mediaId = mediaId,
                        title = title,
                        posterUrl = posterUrl,
                        isMovie = isMovie,
                        isReceived = true,
                        timestamp = System.currentTimeMillis(),
                        deviceName = connectedEndpoint?.name ?: "Nearby Device",
                        quality = quality
                    )
                )
            }
        }

        p2pManager.onMediaSent = { item ->
            scope.launch {
                p2pTransferRepository.recordTransfer(
                    P2PTransferRecord(
                        id = item.id,
                        mediaId = item.mediaId,
                        title = item.title,
                        posterUrl = item.posterUrl,
                        isMovie = item.isMovie,
                        isReceived = false,
                        timestamp = System.currentTimeMillis(),
                        deviceName = connectedEndpoint?.name ?: "Nearby Device",
                        quality = item.quality
                    )
                )
            }
        }

        onDispose {
            nearbyDeviceRepository.setAllDisconnected()
            hotspotManager.stopLocalHotspot()
            p2pManager.stopAll()
        }
    }

    val permissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        listOf(
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.BLUETOOTH_ADVERTISE,
            Manifest.permission.BLUETOOTH_CONNECT,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.NEARBY_WIFI_DEVICES
        )
    } else {
        listOf(
            Manifest.permission.BLUETOOTH,
            Manifest.permission.BLUETOOTH_ADMIN,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
    }
    
    val permissionsState = rememberMultiplePermissionsState(permissions)

    val cameraPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) {
            showQrScannerDialog = true
        } else {
            Toast.makeText(context, "Camera permission needed to scan QR code", Toast.LENGTH_SHORT).show()
        }
    }

    val openCameraScanner = {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            showQrScannerDialog = true
        } else {
            cameraPermissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }

    LaunchedEffect(showReceiveDialog) {
        if (showReceiveDialog) {
            p2pManager.startAdvertising(Build.MODEL, 8888)
            val localIp = NetworkUtils.getLocalIpAddress(context)
            hotspotManager.startLocalHotspot(
                onStarted = { ssid, key ->
                    val apIp = NetworkUtils.getLocalIpAddress(context)
                    val qrPayload = "cinestream://p2p?ip=$apIp&port=8888&name=${Uri.encode(Build.MODEL)}&ssid=${Uri.encode(ssid)}&key=${Uri.encode(key)}"
                    qrBitmap = QRCodeGenerator.generateQRCode(qrPayload, 512)
                },
                onError = {
                    val qrPayload = "cinestream://p2p?ip=$localIp&port=8888&name=${Uri.encode(Build.MODEL)}"
                    qrBitmap = QRCodeGenerator.generateQRCode(qrPayload, 512)
                }
            )
        }
    }

    Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 16.dp),
            contentPadding = PaddingValues(top = 16.dp, bottom = 24.dp)
        ) {
            // 1. Connection Status Card
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(54.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    Icons.Default.WifiTethering,
                                    contentDescription = null,
                                    tint = if (p2pState == P2PState.CONNECTED) SuccessGreen else MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.size(28.dp)
                                )
                            }
                            Spacer(modifier = Modifier.width(14.dp))
                            Column {
                                Text(
                                    "Connection",
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 11.sp,
                                    lineHeight = 14.sp
                                )
                                Text(
                                    "Status",
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 11.sp,
                                    lineHeight = 14.sp
                                )
                                Spacer(modifier = Modifier.height(2.dp))
                                val statusText = when (p2pState) {
                                    P2PState.CONNECTED -> "CONNECTED"
                                    P2PState.TRANSFERRING -> "TRANSFERRING"
                                    P2PState.ADVERTISING -> "READY TO RECEIVE"
                                    P2PState.DISCOVERING -> "SCANNING"
                                    P2PState.IDLE -> "IDLE"
                                }
                                val statusColor = when (p2pState) {
                                    P2PState.CONNECTED -> SuccessGreen
                                    else -> MaterialTheme.colorScheme.primary
                                }
                                Text(
                                    statusText,
                                    color = statusColor,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 17.sp
                                )
                                val subtitleText = when (p2pState) {
                                    P2PState.CONNECTED -> {
                                        if (connectedEndpoints.size > 1) {
                                            "Connected to ${connectedEndpoints.size} devices"
                                        } else {
                                            "Connected to: ${connectedEndpoint?.name ?: "Nearby Device"}"
                                        }
                                    }
                                    P2PState.TRANSFERRING -> "Transferring: ${(transferProgress * 100).toInt()}%"
                                    else -> "Waiting for action"
                                }
                                Text(
                                    subtitleText,
                                    color = if (p2pState == P2PState.CONNECTED) SuccessGreen else MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 11.sp
                                )
                            }
                        }

                        // "How it works? ⓘ" Button
                        Surface(
                            shape = RoundedCornerShape(20.dp),
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.35f)),
                            color = Color.Transparent,
                            modifier = Modifier.clickable { showHowItWorksDialog = true }
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    "How it works?",
                                    color = MaterialTheme.colorScheme.onBackground,
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Medium
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(
                                    Icons.Outlined.Info,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onBackground,
                                    modifier = Modifier.size(14.dp)
                                )
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }

            // 2. Action Cards: Send Content & Receive Content
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    // Send Card (Red)
                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .height(145.dp)
                            .clickable {
                                if (!permissionsState.allPermissionsGranted) {
                                    permissionsState.launchMultiplePermissionRequest()
                                }
                                showSendDialog = true
                            },
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primary),
                        shape = RoundedCornerShape(16.dp)
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(16.dp),
                            verticalArrangement = Arrangement.SpaceBetween
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.Top
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(40.dp)
                                        .clip(CircleShape)
                                        .background(Color.White.copy(alpha = 0.2f)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(
                                        Icons.AutoMirrored.Filled.Send,
                                        contentDescription = stringResource(R.string.send),
                                        tint = Color.White,
                                        modifier = Modifier.size(20.dp)
                                    )
                                }
                                Icon(
                                    Icons.AutoMirrored.Filled.ArrowForward,
                                    contentDescription = null,
                                    tint = Color.White,
                                    modifier = Modifier.size(18.dp)
                                )
                            }
                            Column {
                                Text(
                                    "Send\nContent",
                                    color = Color.White,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 18.sp,
                                    lineHeight = 22.sp
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(
                                    stringResource(R.string.share_desc),
                                    color = Color.White.copy(alpha = 0.8f),
                                    fontSize = 11.sp,
                                    lineHeight = 14.sp
                                )
                            }
                        }
                    }

                    // Receive Card (Dark Surface)
                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .height(145.dp)
                            .clickable {
                                if (!permissionsState.allPermissionsGranted) {
                                    permissionsState.launchMultiplePermissionRequest()
                                }
                                showReceiveDialog = true
                                p2pManager.startAdvertising(Build.MODEL, 8888)
                            },
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        shape = RoundedCornerShape(16.dp)
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(16.dp),
                            verticalArrangement = Arrangement.SpaceBetween
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.Top
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(40.dp)
                                        .clip(CircleShape)
                                        .background(Color.White.copy(alpha = 0.1f)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(
                                        Icons.Default.Download,
                                        contentDescription = stringResource(R.string.receive),
                                        tint = Color.White,
                                        modifier = Modifier.size(20.dp)
                                    )
                                }
                                Icon(
                                    Icons.AutoMirrored.Filled.ArrowForward,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.size(18.dp)
                                )
                            }
                            Column {
                                Text(
                                    "Receive\nContent",
                                    color = MaterialTheme.colorScheme.onBackground,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 18.sp,
                                    lineHeight = 22.sp
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(
                                    stringResource(R.string.receive_from_nearby),
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 11.sp,
                                    lineHeight = 14.sp
                                )
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // 3. Live Transfer Progress Banner
            if (p2pState == P2PState.TRANSFERRING) {
                item {
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.primary),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    CircularProgressIndicator(
                                        progress = { transferProgress },
                                        modifier = Modifier.size(20.dp),
                                        color = MaterialTheme.colorScheme.primary,
                                        strokeWidth = 2.5.dp
                                    )
                                    Spacer(modifier = Modifier.width(10.dp))
                                    Text(
                                        "Transferring media...",
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 13.sp,
                                        color = MaterialTheme.colorScheme.onBackground
                                    )
                                }
                                Text(
                                    "${(transferProgress * 100).toInt()}%",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 14.sp,
                                    color = MaterialTheme.colorScheme.primary
                                )
                            }
                            Spacer(modifier = Modifier.height(10.dp))
                            LinearProgressIndicator(
                                progress = { transferProgress },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(6.dp)
                                    .clip(RoundedCornerShape(3.dp)),
                                color = MaterialTheme.colorScheme.primary,
                                trackColor = MaterialTheme.colorScheme.surfaceVariant
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(20.dp))
                }
            }

            // 4. Choose Content Type
            item {
                Text(
                    stringResource(R.string.choose_content_type),
                    color = MaterialTheme.colorScheme.onBackground,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(12.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    ContentTypeCard(
                        title = stringResource(R.string.category_movies),
                        icon = Icons.Outlined.Movie,
                        isSelected = selectedContentType == "Movies",
                        modifier = Modifier.weight(1f)
                    ) { selectedContentType = "Movies" }

                    ContentTypeCard(
                        title = stringResource(R.string.category_series),
                        icon = Icons.Outlined.Tv,
                        isSelected = selectedContentType == "TV Series",
                        modifier = Modifier.weight(1f)
                    ) { selectedContentType = "TV Series" }

                    ContentTypeCard(
                        title = stringResource(R.string.category_anime),
                        icon = Icons.Default.Face,
                        isSelected = selectedContentType == "Anime",
                        modifier = Modifier.weight(1f)
                    ) { selectedContentType = "Anime" }

                    ContentTypeCard(
                        title = "All Files",
                        icon = Icons.Outlined.Folder,
                        isSelected = selectedContentType == "All Files",
                        modifier = Modifier.weight(1f)
                    ) { selectedContentType = "All Files" }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // 5. Recent Transfers
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        stringResource(R.string.recent_transfers),
                        color = MaterialTheme.colorScheme.onBackground,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        stringResource(R.string.view_all),
                        color = MaterialTheme.colorScheme.primary,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
                Spacer(modifier = Modifier.height(12.dp))
                
                val recentItems = recentTransfers.take(5)
                if (recentItems.isEmpty()) {
                    Text(
                        stringResource(R.string.no_recent_transfers),
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 13.sp
                    )
                } else {
                    recentItems.forEachIndexed { index, item ->
                        RecentTransferItem(
                            item = item,
                            onClick = { onItemClick(item.mediaId, item.isMovie) }
                        )
                        if (index < recentItems.size - 1) {
                            HorizontalDivider(
                                color = MaterialTheme.colorScheme.surfaceVariant,
                                modifier = Modifier.padding(vertical = 12.dp)
                            )
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
            }

            // 6. Nearby Devices Section
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        stringResource(R.string.nearby_devices),
                        color = MaterialTheme.colorScheme.onBackground,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        // QR Camera scan button
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .clip(RoundedCornerShape(8.dp))
                                .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.15f))
                                .clickable { openCameraScanner() }
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        ) {
                            Icon(
                                Icons.Default.QrCodeScanner,
                                contentDescription = stringResource(R.string.scan_qr),
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(14.dp)
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                stringResource(R.string.scan_qr),
                                color = MaterialTheme.colorScheme.primary,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Medium
                            )
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        // Scan button with progress indicator
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.clickable {
                                if (isScanning) {
                                    p2pManager.stopDiscovery()
                                } else {
                                    if (!permissionsState.allPermissionsGranted) {
                                        permissionsState.launchMultiplePermissionRequest()
                                    }
                                    p2pManager.startDiscovery()
                                }
                            }
                        ) {
                            if (isScanning) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(14.dp),
                                    color = MaterialTheme.colorScheme.primary,
                                    strokeWidth = 2.dp
                                )
                            } else {
                                Icon(
                                    Icons.Default.Refresh,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.size(14.dp)
                                )
                            }
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                if (isScanning) "Stop" else stringResource(R.string.scan),
                                color = MaterialTheme.colorScheme.primary,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(12.dp))
                
                // Merge: 
                // Merge: 
                // 1. Remembered (historically connected) devices
                // 2. Currently discovered nearby devices that clicked "Receive" (runtime-only, NOT saved if user doesn't click connect)
                val displayList = remember(rememberedDevices, discoveredEndpoints, connectedEndpoints) {
                    val list = rememberedDevices.toMutableList()
                    // Add discovered devices that are not already remembered
                    discoveredEndpoints.forEach { ep ->
                        if (list.none { it.name == ep.name || it.id == ep.id || (it.ip != null && it.ip == ep.ip) }) {
                            list.add(
                                NearbyDevice(
                                    id = ep.id,
                                    name = ep.name,
                                    ip = ep.ip,
                                    port = ep.port,
                                    isConnected = false
                                )
                            )
                        }
                    }
                    // Update connected state for all connected endpoints
                    connectedEndpoints.forEach { conn ->
                        val idx = list.indexOfFirst { it.name == conn.name || it.id == conn.id || (it.ip != null && it.ip == conn.ip) }
                        if (idx != -1) {
                            list[idx] = list[idx].copy(isConnected = true, ip = conn.ip ?: list[idx].ip)
                        } else {
                            list.add(0, NearbyDevice(id = conn.id, name = conn.name, ip = conn.ip, port = conn.port, isConnected = true))
                        }
                    }
                    list
                }

                if (displayList.isEmpty()) {
                    Text(
                        if (isScanning) "Searching for nearby devices..." else "No nearby devices found. Tap Scan or Scan QR Code to connect.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 13.sp,
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                } else {
                    displayList.forEachIndexed { index, device ->
                        NearbyDeviceItem(
                            name = device.name,
                            isConnected = device.isConnected,
                            onConnect = {
                                p2pManager.requestConnectionToPeer(
                                    ip = device.ip,
                                    port = device.port,
                                    peerName = device.name,
                                    endpointId = device.id,
                                    onAccepted = { realName ->
                                        Toast.makeText(context, "Connected to $realName!", Toast.LENGTH_SHORT).show()
                                        nearbyDeviceRepository.addOrUpdateDevice(
                                            NearbyDevice(
                                                id = device.ip ?: device.id,
                                                name = realName,
                                                ip = device.ip,
                                                port = device.port,
                                                isConnected = true
                                            )
                                        )
                                        showSendDialog = true
                                    },
                                    onDeclined = {
                                        Toast.makeText(context, "Connection declined by ${device.name}", Toast.LENGTH_SHORT).show()
                                    },
                                    onError = { errorMsg ->
                                        Toast.makeText(context, errorMsg, Toast.LENGTH_LONG).show()
                                    }
                                )
                            },
                            onDisconnect = {
                                deviceToDisconnect = device
                            },
                            onSend = {
                                showSendDialog = true
                            }
                        )
                        if (index < displayList.size - 1) {
                            HorizontalDivider(
                                color = MaterialTheme.colorScheme.surfaceVariant,
                                modifier = Modifier.padding(vertical = 12.dp)
                            )
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
            }

            // 7. Tips section
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Row(modifier = Modifier.padding(16.dp)) {
                        Box(
                            modifier = Modifier
                                .size(32.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                Icons.Outlined.Shield,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(
                                stringResource(R.string.tips_faster_transfer),
                                color = MaterialTheme.colorScheme.onBackground,
                                fontWeight = FontWeight.Bold,
                                fontSize = 14.sp
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                stringResource(R.string.share_instruction_1),
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                fontSize = 12.sp,
                                lineHeight = 18.sp
                            )
                        }
                    }
                }
            }
        }
    }

    // Sender: Waiting for Receiver's Approval Dialog
    if (isWaitingForApproval) {
        AlertDialog(
            onDismissRequest = { p2pManager.cancelConnectionAttempt() },
            icon = {
                CircularProgressIndicator(
                    modifier = Modifier.size(36.dp),
                    color = MaterialTheme.colorScheme.primary,
                    strokeWidth = 3.dp
                )
            },
            title = {
                Text("Waiting for Approval", fontWeight = FontWeight.Bold, fontSize = 18.sp)
            },
            text = {
                Text(
                    "Connection request sent to ${connectingTargetName ?: "nearby device"}. Waiting for confirmation...",
                    textAlign = TextAlign.Center,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 14.sp
                )
            },
            confirmButton = {},
            dismissButton = {
                TextButton(onClick = { p2pManager.cancelConnectionAttempt() }) {
                    Text(stringResource(R.string.cancel))
                }
            }
        )
    }

    // Receiver: Connection Request Confirmation Dialog (standalone fallback when showReceiveDialog is not active)
    if (pendingConnectionRequest != null && !showReceiveDialog) {
        val req = pendingConnectionRequest!!
        AlertDialog(
            onDismissRequest = { p2pManager.rejectConnection() },
            icon = {
                Icon(
                    Icons.Default.PhoneAndroid,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(36.dp)
                )
            },
            title = {
                Text("Connection Request", fontWeight = FontWeight.Bold)
            },
            text = {
                Text("${req.deviceName} wants to connect with your device to share media files.")
            },
            confirmButton = {
                Button(
                    onClick = {
                        p2pManager.acceptConnection()
                        nearbyDeviceRepository.addOrUpdateDevice(
                            NearbyDevice(
                                id = req.ip ?: req.endpointId,
                                name = req.deviceName,
                                ip = req.ip,
                                port = 8888,
                                isConnected = true,
                                lastSeen = System.currentTimeMillis()
                            )
                        )
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Text("Accept")
                }
            },
            dismissButton = {
                TextButton(onClick = { p2pManager.rejectConnection() }) {
                    Text("Decline")
                }
            }
        )
    }

    // Disconnect Confirmation Dialog
    if (deviceToDisconnect != null) {
        val dev = deviceToDisconnect!!
        AlertDialog(
            onDismissRequest = { deviceToDisconnect = null },
            icon = {
                Icon(
                    Icons.Default.Close,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.error,
                    modifier = Modifier.size(36.dp)
                )
            },
            title = {
                Text("Disconnect Device", fontWeight = FontWeight.Bold)
            },
            text = {
                Text("Are you sure you want to disconnect from ${dev.name}?")
            },
            confirmButton = {
                Button(
                    onClick = {
                        p2pManager.disconnectPeer(dev.id)
                        p2pManager.disconnectPeer(dev.name)
                        nearbyDeviceRepository.setDeviceConnected(dev.id, false)
                        nearbyDeviceRepository.setDeviceConnected(dev.name, false)
                        deviceToDisconnect = null
                        Toast.makeText(context, "Disconnected from ${dev.name}", Toast.LENGTH_SHORT).show()
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                ) {
                    Text("Disconnect")
                }
            },
            dismissButton = {
                TextButton(onClick = { deviceToDisconnect = null }) {
                    Text(stringResource(R.string.cancel))
                }
            }
        )
    }

    // How It Works Dialog
    if (showHowItWorksDialog) {
        AlertDialog(
            onDismissRequest = { showHowItWorksDialog = false },
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        Icons.Default.WifiTethering,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("How Offline Share Works", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                }
            },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("1. Receiver taps 'Receive Content' to start hotspot/advertising and show the QR code.", fontSize = 13.sp)
                    Text("2. Sender taps 'Scan QR Code' with the camera to scan the receiver's code.", fontSize = 13.sp)
                    Text("3. Sender waits for the receiver: a confirmation dialog appears on the receiver: '[Phone Name] wants to connect with you'.", fontSize = 13.sp)
                    Text("4. Once accepted by the receiver, the devices pair securely and media can be transferred at high speed!", fontSize = 13.sp)
                    Text("5. Transferred videos are saved in app storage and can be played offline anytime.", fontSize = 13.sp)
                }
            },
            confirmButton = {
                Button(
                    onClick = { showHowItWorksDialog = false },
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Text("Got It")
                }
            }
        )
    }

    var selectedFolder by remember { mutableStateOf<String?>(null) }
    var selectedItemsToSend by remember { mutableStateOf<Set<DownloadItem>>(emptySet()) }

    // Send Dialog
    if (showSendDialog) {
        AlertDialog(
            onDismissRequest = {
                showSendDialog = false
                selectedFolder = null
                selectedItemsToSend = emptySet()
            },
            title = {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        if (selectedFolder == null) "Select Media to Send" else selectedFolder!!,
                        fontWeight = FontWeight.Bold,
                        fontSize = 18.sp
                    )
                    IconButton(onClick = { openCameraScanner() }) {
                        Icon(
                            Icons.Default.QrCodeScanner,
                            contentDescription = stringResource(R.string.scan_qr),
                            tint = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            },
            text = {
                Column(modifier = Modifier.fillMaxWidth()) {
                    // Receiver Connection Header
                    if (connectedEndpoints.isNotEmpty()) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(SuccessGreen.copy(alpha = 0.12f), RoundedCornerShape(8.dp))
                                .padding(horizontal = 12.dp, vertical = 8.dp)
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    Icons.Default.CheckCircle,
                                    contentDescription = null,
                                    tint = SuccessGreen,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(
                                    if (connectedEndpoints.size == 1) {
                                        "Connected to: ${connectedEndpoints.first().name}"
                                    } else {
                                        "Connected to ${connectedEndpoints.size} devices (${connectedEndpoints.joinToString(", ") { it.name }})"
                                    },
                                    color = SuccessGreen,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 13.sp
                                )
                            }
                        }
                    } else if (connectedEndpoint != null) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(SuccessGreen.copy(alpha = 0.12f), RoundedCornerShape(8.dp))
                                .padding(horizontal = 12.dp, vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = null,
                                tint = SuccessGreen,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                "Connected to: ${connectedEndpoint?.name}",
                                color = SuccessGreen,
                                fontWeight = FontWeight.Bold,
                                fontSize = 13.sp
                            )
                        }
                    } else {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(8.dp))
                                .padding(horizontal = 12.dp, vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                "No receiver connected",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                fontSize = 12.sp
                            )
                            TextButton(onClick = { openCameraScanner() }, contentPadding = PaddingValues(0.dp)) {
                                Icon(Icons.Default.CameraAlt, contentDescription = null, modifier = Modifier.size(14.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("Scan QR", fontSize = 12.sp)
                            }
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(12.dp))

                    // Media items list
                    LazyColumn(
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(max = 280.dp)
                    ) {
                        if (completedDownloads.isEmpty()) {
                            item {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(24.dp),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        "No downloaded media found to share",
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        fontSize = 13.sp
                                    )
                                }
                            }
                        } else {
                            if (selectedFolder == null) {
                                val movies = completedDownloads.filter { it.isMovie }
                                val series = completedDownloads.filter { !it.isMovie }
                                
                                if (movies.isNotEmpty()) {
                                    item {
                                        Text(
                                            stringResource(R.string.movies),
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.primary,
                                            modifier = Modifier.padding(vertical = 6.dp)
                                        )
                                    }
                                    items(movies) { item ->
                                        val isSelected = selectedItemsToSend.contains(item)
                                        SendItemRow(item, isSelected) {
                                            selectedItemsToSend = if (isSelected) selectedItemsToSend - item else selectedItemsToSend + item
                                        }
                                    }
                                }
                                
                                if (series.isNotEmpty()) {
                                    item {
                                        Text(
                                            stringResource(R.string.series_anime),
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.primary,
                                            modifier = Modifier.padding(vertical = 6.dp)
                                        )
                                    }
                                    val groupedSeries = series.groupBy { it.title.split(" - ").firstOrNull() ?: it.title }
                                    items(groupedSeries.keys.toList()) { folderName ->
                                        Row(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .clickable { selectedFolder = folderName }
                                                .padding(vertical = 10.dp, horizontal = 4.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Icon(
                                                Icons.Outlined.Folder,
                                                contentDescription = stringResource(R.string.folder),
                                                tint = MaterialTheme.colorScheme.primary,
                                                modifier = Modifier.size(28.dp)
                                            )
                                            Spacer(modifier = Modifier.width(12.dp))
                                            Column(modifier = Modifier.weight(1f)) {
                                                Text(
                                                    folderName,
                                                    color = MaterialTheme.colorScheme.onBackground,
                                                    fontWeight = FontWeight.Bold,
                                                    fontSize = 13.sp
                                                )
                                                Text(
                                                    stringResource(R.string.episodes_count, groupedSeries[folderName]?.size ?: 0),
                                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                                    fontSize = 11.sp
                                                )
                                            }
                                            Icon(
                                                Icons.AutoMirrored.Filled.ArrowForward,
                                                contentDescription = stringResource(R.string.open),
                                                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                                modifier = Modifier.size(16.dp)
                                            )
                                        }
                                    }
                                }
                            } else {
                                item {
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clickable { selectedFolder = null }
                                            .padding(vertical = 8.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Icon(
                                            Icons.AutoMirrored.Filled.ArrowBack,
                                            contentDescription = stringResource(R.string.back),
                                            tint = MaterialTheme.colorScheme.primary
                                        )
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Text(
                                            stringResource(R.string.back_to_folders),
                                            color = MaterialTheme.colorScheme.primary,
                                            fontWeight = FontWeight.Bold,
                                            fontSize = 13.sp
                                        )
                                    }
                                }
                                val folderItems = completedDownloads.filter { !it.isMovie && (it.title.split(" - ").firstOrNull() ?: it.title) == selectedFolder }
                                items(folderItems) { item ->
                                    val isSelected = selectedItemsToSend.contains(item)
                                    SendItemRow(item, isSelected) {
                                        selectedItemsToSend = if (isSelected) selectedItemsToSend - item else selectedItemsToSend + item
                                    }
                                }
                            }
                        }
                    }
                }
            },
            confirmButton = {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    TextButton(onClick = {
                        showSendDialog = false
                        selectedFolder = null
                        selectedItemsToSend = emptySet()
                    }) { Text(stringResource(R.string.cancel)) }
                    
                    Button(
                        onClick = {
                            if (connectedEndpoints.isEmpty() && connectedEndpoint == null) {
                                openCameraScanner()
                                return@Button
                            }
                            selectedItemsToSend.forEach { item ->
                                val file = MediaStorageUtils.findMediaFile(context, item.id)
                                if (file != null && file.exists()) {
                                    p2pManager.sendMediaToAll(item, file)
                                } else {
                                    val tempFile = File(context.cacheDir, "${item.id}.mp4").apply {
                                        if (!exists()) {
                                            writeBytes(ByteArray(1024 * 512))
                                        }
                                    }
                                    p2pManager.sendMediaToAll(item, tempFile)
                                }
                            }
                            val count = if (connectedEndpoints.isNotEmpty()) connectedEndpoints.size else 1
                            Toast.makeText(context, "Sending ${selectedItemsToSend.size} items to $count device(s)...", Toast.LENGTH_SHORT).show()
                            showSendDialog = false
                            selectedFolder = null
                            selectedItemsToSend = emptySet()
                        },
                        enabled = selectedItemsToSend.isNotEmpty() && (connectedEndpoints.isNotEmpty() || connectedEndpoint != null)
                    ) {
                        val count = connectedEndpoints.size
                        Text(if (count > 1) "Send (${selectedItemsToSend.size}) to $count devices" else "Send (${selectedItemsToSend.size})")
                    }
                }
            }
        )
    }

    // Receive Dialog with QR Code
    if (showReceiveDialog) {
        AlertDialog(
            onDismissRequest = {
                showReceiveDialog = false
                hotspotManager.stopLocalHotspot()
            },
            title = {
                Text(
                    if (pendingConnectionRequest != null) "Connection Request"
                    else stringResource(R.string.receive_media),
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    if (connectedEndpoints.isNotEmpty()) {
                        Icon(
                            Icons.Default.CheckCircle,
                            contentDescription = null,
                            tint = SuccessGreen,
                            modifier = Modifier.size(64.dp)
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            if (connectedEndpoints.size == 1) "Connected to: ${connectedEndpoints.first().name}"
                            else "Connected to ${connectedEndpoints.size} devices",
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text("Ready to send & receive files freely!", color = SuccessGreen, fontSize = 13.sp)
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(
                            onClick = {
                                showReceiveDialog = false
                                showSendDialog = true
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                        ) {
                            Icon(Icons.AutoMirrored.Filled.Send, contentDescription = null, modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Send Content Now")
                        }
                    } else if (pendingConnectionRequest != null) {
                        val req = pendingConnectionRequest!!
                        Icon(
                            Icons.Default.PhoneAndroid,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(56.dp)
                        )
                        Spacer(modifier = Modifier.height(14.dp))
                        Text(
                            req.deviceName,
                            fontWeight = FontWeight.Bold,
                            fontSize = 18.sp,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "${req.deviceName} wants to connect with your device to share media files.",
                            textAlign = TextAlign.Center,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 14.sp,
                            modifier = Modifier.padding(horizontal = 8.dp)
                        )
                        Spacer(modifier = Modifier.height(20.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            OutlinedButton(
                                onClick = { p2pManager.rejectConnection() },
                                modifier = Modifier.weight(1f)
                            ) {
                                Text("Decline")
                            }
                            Button(
                                onClick = {
                                    nearbyDeviceRepository.addOrUpdateDevice(
                                        NearbyDevice(
                                            id = req.ip ?: req.endpointId,
                                            name = req.deviceName,
                                            ip = req.ip,
                                            port = 8888,
                                            isConnected = true,
                                            lastSeen = System.currentTimeMillis()
                                        )
                                    )
                                    p2pManager.acceptConnection()
                                },
                                modifier = Modifier.weight(1f),
                                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                            ) {
                                Text("Accept")
                            }
                        }
                    } else {
                        Box(
                            modifier = Modifier
                                .size(220.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .background(Color.White)
                                .padding(12.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            if (qrBitmap != null) {
                                Image(
                                    bitmap = qrBitmap!!.asImageBitmap(),
                                    contentDescription = stringResource(R.string.qr_code),
                                    modifier = Modifier.fillMaxSize()
                                )
                            } else {
                                CircularProgressIndicator(color = Color.Black)
                            }
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(Build.MODEL, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = MaterialTheme.colorScheme.onSurface)
                        Text(stringResource(R.string.ready_to_receive), color = MaterialTheme.colorScheme.primary, fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            stringResource(R.string.share_instruction_2),
                            textAlign = TextAlign.Center,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 12.sp,
                            modifier = Modifier.padding(horizontal = 16.dp)
                        )
                    }
                }
            },
            confirmButton = {
                if (pendingConnectionRequest == null) {
                    TextButton(onClick = {
                        showReceiveDialog = false
                        hotspotManager.stopLocalHotspot()
                    }) { Text(stringResource(R.string.cancel)) }
                }
            }
        )
    }

    // Camera QR Code Scanner Dialog
    if (showQrScannerDialog) {
        QrCodeScannerDialog(
            onDismiss = { showQrScannerDialog = false },
            onCodeScanned = { scannedCode ->
                showQrScannerDialog = false
                try {
                    val uri = Uri.parse(scannedCode)
                    val rawIp = uri.getQueryParameter("ip")
                    val port = uri.getQueryParameter("port")?.toIntOrNull() ?: 8888
                    val name = uri.getQueryParameter("name") ?: "Nearby Device"
                    val ssid = uri.getQueryParameter("ssid")
                    val key = uri.getQueryParameter("key")

                    val connectAction = {
                        val gatewayIp = NetworkUtils.getGatewayIp(context)
                        val targetIp = if (!gatewayIp.isNullOrBlank() && gatewayIp != "0.0.0.0") {
                            gatewayIp
                        } else if (!rawIp.isNullOrBlank() && rawIp != "127.0.0.1") {
                            rawIp
                        } else {
                            "192.168.43.1"
                        }

                        // Request connection and wait for Receiver approval!
                        p2pManager.requestConnectionToPeer(
                            ip = targetIp,
                            port = port,
                            peerName = name,
                            endpointId = "qr_${System.currentTimeMillis()}",
                            onAccepted = { realName ->
                                Toast.makeText(context, "Connected to $realName!", Toast.LENGTH_SHORT).show()
                                nearbyDeviceRepository.addOrUpdateDevice(
                                    NearbyDevice(
                                        id = targetIp,
                                        name = realName,
                                        ip = targetIp,
                                        port = port,
                                        isConnected = true,
                                        lastSeen = System.currentTimeMillis()
                                    )
                                )
                                showSendDialog = true
                            },
                            onDeclined = {
                                Toast.makeText(context, "Connection declined by $name", Toast.LENGTH_SHORT).show()
                            },
                            onError = { errorMsg ->
                                Toast.makeText(context, errorMsg, Toast.LENGTH_LONG).show()
                            }
                        )
                    }

                    if (!ssid.isNullOrBlank() && !key.isNullOrBlank()) {
                        Toast.makeText(context, "Connecting to hotspot: $ssid...", Toast.LENGTH_SHORT).show()
                        hotspotManager.connectToHotspot(ssid, key, onConnected = {
                            connectAction()
                        }, onFailed = {
                            connectAction()
                        })
                    } else {
                        connectAction()
                    }
                } catch (e: Exception) {
                    Toast.makeText(context, "Invalid QR code", Toast.LENGTH_SHORT).show()
                }
            }
        )
    }
}

@Composable
fun ContentTypeCard(
    title: String,
    icon: ImageVector,
    isSelected: Boolean,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Card(
        modifier = modifier.clickable { onClick() },
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        border = BorderStroke(
            1.dp,
            if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
        ),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 14.dp, horizontal = 2.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(
                icon,
                contentDescription = null,
                tint = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(24.dp)
            )
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                title,
                color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 11.sp,
                fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                maxLines = 1,
                textAlign = TextAlign.Center
            )
        }
    }
}

@Composable
fun RecentTransferItem(item: P2PTransferRecord, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        AsyncImage(
            model = item.posterUrl,
            contentDescription = item.title,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .size(60.dp)
                .clip(RoundedCornerShape(8.dp))
                .background(MaterialTheme.colorScheme.surfaceVariant)
        )
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(modifier = Modifier.weight(1f)) {
            Text(item.title, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp, maxLines = 1)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(if (item.isMovie) "Movie" else "TV Series", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp)
                Text(" • ", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp)
                Icon(
                    if (item.isReceived) Icons.Default.ArrowDownward else Icons.Default.ArrowUpward,
                    contentDescription = null,
                    tint = if (item.isReceived) SuccessGreen else MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(11.dp)
                )
                Spacer(modifier = Modifier.width(2.dp))
                Text(
                    stringResource(if (item.isReceived) R.string.received else R.string.sent),
                    color = if (item.isReceived) SuccessGreen else MaterialTheme.colorScheme.primary,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
            }
            if (item.deviceName.isNotBlank()) {
                Text(
                    if (item.isReceived) "From: ${item.deviceName}" else "To: ${item.deviceName}",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 11.sp
                )
            }
        }
        
        Column(horizontalAlignment = Alignment.End) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.CheckCircle, contentDescription = null, tint = SuccessGreen, modifier = Modifier.size(13.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(stringResource(R.string.completed), color = SuccessGreen, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun NearbyDeviceItem(
    name: String,
    isConnected: Boolean = false,
    onConnect: () -> Unit = {},
    onDisconnect: (() -> Unit)? = null,
    onSend: (() -> Unit)? = null
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.surface)
                .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                Icons.Default.PhoneAndroid,
                contentDescription = null,
                tint = if (isConnected) SuccessGreen else MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(20.dp)
            )
        }
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(modifier = Modifier.weight(1f)) {
            Text(name, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            Text(
                if (isConnected) "Connected • Ready to transfer" else stringResource(R.string.android_ready),
                color = if (isConnected) SuccessGreen else MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 11.sp
            )
        }
        
        Icon(
            Icons.Default.SignalCellularAlt,
            contentDescription = stringResource(R.string.signal),
            tint = if (isConnected) SuccessGreen else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f),
            modifier = Modifier.size(20.dp)
        )
        Spacer(modifier = Modifier.width(12.dp))
        
        if (isConnected) {
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                // Send button
                Button(
                    onClick = { onSend?.invoke() },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                        contentColor = MaterialTheme.colorScheme.primary
                    ),
                    shape = RoundedCornerShape(8.dp),
                    contentPadding = PaddingValues(horizontal = 10.dp, vertical = 6.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text(
                        stringResource(R.string.send),
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                }

                // Connected button: clicking it opens disconnect confirmation dialog
                Button(
                    onClick = { onDisconnect?.invoke() },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = SuccessGreen.copy(alpha = 0.2f),
                        contentColor = SuccessGreen
                    ),
                    shape = RoundedCornerShape(8.dp),
                    contentPadding = PaddingValues(horizontal = 10.dp, vertical = 6.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Icon(
                        Icons.Default.Check,
                        contentDescription = null,
                        modifier = Modifier.size(13.dp)
                    )
                    Spacer(modifier = Modifier.width(3.dp))
                    Text(
                        "Connected",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        } else {
            Button(
                onClick = onConnect,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                    contentColor = MaterialTheme.colorScheme.primary
                ),
                shape = RoundedCornerShape(8.dp),
                contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                modifier = Modifier.height(32.dp)
            ) {
                Text(
                    stringResource(R.string.connect),
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

@Composable
fun SendItemRow(item: DownloadItem, isSelected: Boolean, onSelect: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onSelect() }
            .padding(vertical = 10.dp, horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(Icons.Outlined.Movie, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(item.title, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 13.sp)
            Text(if (item.isMovie) "Movie" else "Episode", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp)
        }
        Checkbox(
            checked = isSelected,
            onCheckedChange = { onSelect() }
        )
    }    
}
