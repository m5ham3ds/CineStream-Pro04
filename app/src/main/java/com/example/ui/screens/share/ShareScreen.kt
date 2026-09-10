package com.example.ui.screens.share

import android.Manifest
import android.os.Build
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
import androidx.compose.material.icons.outlined.QrCode2
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Tv
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.data.model.DownloadItem
import com.example.data.repository.DownloadRepository
import com.example.utils.Endpoint
import com.example.utils.P2PManager
import com.example.utils.P2PState
import com.google.accompanist.permissions.ExperimentalPermissionsApi
import com.google.accompanist.permissions.rememberMultiplePermissionsState
import kotlinx.coroutines.launch
import java.io.File
import androidx.compose.foundation.lazy.LazyRow

@OptIn(ExperimentalPermissionsApi::class, ExperimentalMaterial3Api::class)
@Composable
fun ShareScreen(
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val p2pManager = remember { P2PManager(context) }
    val downloadRepository = remember { com.example.data.repository.DownloadRepository(context) }
    
    val p2pState by p2pManager.p2pState.collectAsState()
    val connectedEndpoint by p2pManager.connectedEndpoint.collectAsState()
    val discoveredEndpoints by p2pManager.discoveredEndpoints.collectAsState()
    val transferProgress by p2pManager.transferProgress.collectAsState()
    
    val allDownloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val completedDownloads = remember(allDownloads) { allDownloads.filter { it.isCompleted } }

    DisposableEffect(Unit) {
        p2pManager.onMovieReceived = { id, title, isMovie, posterUrl ->
            scope.launch {
                downloadRepository.addCompletedDownload(
                    DownloadItem(
                        id = id,
                        title = title,
                        posterUrl = posterUrl,
                        isMovie = isMovie,
                        quality = "1080p", // Inherited default
                        progress = 1f,
                        isCompleted = true
                    )
                )
            }
        }
        onDispose { p2pManager.stopAll() }
    }

    val permissions = if (Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
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
    var showSendDialog by remember { mutableStateOf(false) }
    var showReceiveDialog by remember { mutableStateOf(false) }
    var pendingAction by remember { mutableStateOf<(() -> Unit)?>(null) }
    var selectedContentType by remember { mutableStateOf("Movies") }
    
    // Check permission logic
    val checkPermissionsAndRun = { action: () -> Unit ->
        if (permissionsState.allPermissionsGranted) {
            action()
        } else {
            pendingAction = action
            permissionsState.launchMultiplePermissionRequest()
        }
    }
    
    LaunchedEffect(permissionsState.allPermissionsGranted) {
        if (permissionsState.allPermissionsGranted && pendingAction != null) {
            pendingAction?.invoke()
            pendingAction = null
        }
    }

    Scaffold(
        containerColor = Color(0xFF0F0F11),
        topBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Offline Share", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.weight(1f))
                IconButton(onClick = { /* Help */ }) {
                    Icon(Icons.Default.HelpOutline, contentDescription = "Help", tint = Color.White)
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            contentPadding = PaddingValues(bottom = 24.dp)
        ) {
            // Connection Status Card
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF19191C)),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .border(1.dp, Color.Red.copy(alpha = 0.3f), CircleShape)
                                .background(Color.Red.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.WifiTethering, contentDescription = null, tint = Color.Red, modifier = Modifier.size(32.dp))
                        }
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Connection Status", color = Color.Gray, fontSize = 12.sp)
                            val statusText = when (p2pState) {
                                P2PState.DISCOVERING -> "DISCOVERING"
                                P2PState.ADVERTISING -> "ADVERTISING"
                                P2PState.CONNECTED -> "CONNECTED"
                                P2PState.TRANSFERRING -> "TRANSFERRING"
                                else -> "IDLE"
                            }
                            Text(statusText, color = Color.Red, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                            Text("Waiting for action", color = Color.Gray, fontSize = 12.sp)
                        }
                        
                        OutlinedButton(
                            onClick = { /* How it works */ },
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.White),
                            border = BorderStroke(1.dp, Color.Gray.copy(alpha = 0.5f)),
                            shape = RoundedCornerShape(20.dp),
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Text("How it works?", fontSize = 12.sp)
                            Spacer(modifier = Modifier.width(4.dp))
                            Icon(Icons.Outlined.Info, contentDescription = null, modifier = Modifier.size(14.dp))
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }

            // Action Buttons
            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    // Send Card
                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .clickable {
                                checkPermissionsAndRun {
                                    showSendDialog = true
                                    p2pManager.startDiscovery()
                                }
                            },
                        colors = CardDefaults.cardColors(containerColor = Color(0xFFE50914)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(Color.White.copy(alpha = 0.2f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = Color.White, modifier = Modifier.size(20.dp))
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Send Content", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                Text("Share movies, series or anime", color = Color.White.copy(alpha = 0.8f), fontSize = 11.sp, lineHeight = 14.sp)
                            }
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                        }
                    }

                    // Receive Card
                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .clickable {
                                checkPermissionsAndRun {
                                    showReceiveDialog = true
                                    p2pManager.startAdvertising(Build.MODEL)
                                }
                            },
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF19191C)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(Color.White.copy(alpha = 0.1f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Download, contentDescription = "Receive", tint = Color.White, modifier = Modifier.size(20.dp))
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Receive Content", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                Text("Receive from nearby devices", color = Color.Gray, fontSize = 11.sp, lineHeight = 14.sp)
                            }
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Content Type Selector
            item {
                Text("Choose Content Type", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(12.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    ContentTypeCard("Movies", Icons.Outlined.Movie, selectedContentType == "Movies") { selectedContentType = "Movies" }
                    ContentTypeCard("TV Series", Icons.Outlined.Tv, selectedContentType == "TV Series") { selectedContentType = "TV Series" }
                    ContentTypeCard("Anime", Icons.Default.Face, selectedContentType == "Anime") { selectedContentType = "Anime" }
                    ContentTypeCard("All Files", Icons.Outlined.Folder, selectedContentType == "All Files") { selectedContentType = "All Files" }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Recent Transfers
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Recent Transfers", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Text("View All", color = Color.Red, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                }
                Spacer(modifier = Modifier.height(12.dp))
                
                // Demo item 1
                RecentTransferItem(
                    title = "John Wick 4",
                    type = "Movie",
                    size = "2.1 GB",
                    isSent = true,
                    time = "12:45 PM",
                    targetDevice = "Ahmed's Phone",
                    isCompleted = true
                )
                
                HorizontalDivider(color = Color(0xFF2A2A2E), modifier = Modifier.padding(vertical = 12.dp))
                
                // Demo item 2
                RecentTransferItem(
                    title = "Attack on Titan S4",
                    type = "TV Series",
                    size = "8.7 GB",
                    isSent = false,
                    time = "Yesterday",
                    targetDevice = "Sara's Phone",
                    isCompleted = true
                )
                
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Nearby Devices List
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Nearby Devices", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { p2pManager.startDiscovery() }) {
                        Icon(Icons.Default.Refresh, contentDescription = null, tint = Color.Red, modifier = Modifier.size(14.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Scan", color = Color.Red, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                    }
                }
                Spacer(modifier = Modifier.height(12.dp))
                
                if (discoveredEndpoints.isEmpty()) {
                    // Demo devices based on screenshot
                    NearbyDeviceItem("Ahmed's Phone")
                    HorizontalDivider(color = Color(0xFF2A2A2E), modifier = Modifier.padding(vertical = 12.dp))
                    NearbyDeviceItem("Sara's Phone")
                } else {
                    discoveredEndpoints.forEachIndexed { index, endpoint ->
                        NearbyDeviceItem(endpoint.name) {
                            p2pManager.requestConnection(endpoint.id, Build.MODEL)
                        }
                        if (index < discoveredEndpoints.size - 1) {
                            HorizontalDivider(color = Color(0xFF2A2A2E), modifier = Modifier.padding(vertical = 12.dp))
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Tips section
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF19191C)),
                    border = BorderStroke(1.dp, Color(0xFF2A2A2E))
                ) {
                    Row(modifier = Modifier.padding(16.dp)) {
                        Box(
                            modifier = Modifier.size(32.dp).clip(CircleShape).background(Color.Red.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Outlined.Shield, contentDescription = null, tint = Color.Red, modifier = Modifier.size(16.dp))
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text("Tips for faster transfer", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text("Make sure both devices have Wi-Fi and are close to each other. Large files may take some time to transfer.", color = Color.Gray, fontSize = 12.sp, lineHeight = 18.sp)
                        }
                    }
                }
            }
        }
    }

    var selectedFolder by remember { mutableStateOf<String?>(null) }
    
    // Kept the functional dialogs unchanged logic-wise, but using the dark theme
    if (showSendDialog) {
        AlertDialog(
            onDismissRequest = {
                showSendDialog = false
                selectedFolder = null
                p2pManager.stopAll()
            },
            title = { Text(if (selectedFolder == null) "Select Media to Send" else selectedFolder!!, fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    if (p2pState == P2PState.DISCOVERING && discoveredEndpoints.isEmpty()) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally).padding(16.dp))
                        Text("Looking for devices...", textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
                    } else if (discoveredEndpoints.isNotEmpty() && connectedEndpoint == null) {
                        Text("Available Devices:", fontWeight = FontWeight.Bold, modifier = Modifier.padding(vertical = 8.dp))
                        discoveredEndpoints.forEach { endpoint ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { p2pManager.requestConnection(endpoint.id, Build.MODEL) }
                                    .padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Default.PhoneAndroid, contentDescription = null)
                                Spacer(modifier = Modifier.width(16.dp))
                                Text(endpoint.name)
                            }
                        }
                    } else if (connectedEndpoint != null) {
                        Text("Connected to ${connectedEndpoint?.name}", color = Color.Green, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp)) {
                            if (completedDownloads.isEmpty()) {
                                item { Text("No downloaded movies found.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
                            } else {
                                if (selectedFolder == null) {
                                    val movies = completedDownloads.filter { it.isMovie }
                                    val series = completedDownloads.filter { !it.isMovie }
                                    
                                    if (movies.isNotEmpty()) {
                                        item { Text("Movies", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                        items(movies) { item ->
                                            SendItemRow(item, context, p2pManager, connectedEndpoint) { 
                                                showSendDialog = false 
                                                selectedFolder = null
                                            }
                                        }
                                    }
                                    
                                    if (series.isNotEmpty()) {
                                        item { Text("Series / Anime", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                        val groupedSeries = series.groupBy { it.title.split(" - ").firstOrNull() ?: it.title }
                                        items(groupedSeries.keys.toList()) { folderName ->
                                            Row(
                                                modifier = Modifier
                                                    .fillMaxWidth()
                                                    .clickable { selectedFolder = folderName }
                                                    .padding(vertical = 12.dp, horizontal = 8.dp),
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                Icon(Icons.Outlined.Folder, contentDescription = "Folder", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                                                Spacer(modifier = Modifier.width(16.dp))
                                                Column(modifier = Modifier.weight(1f)) {
                                                    Text(folderName, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                                    Text("${groupedSeries[folderName]?.size ?: 0} Episodes", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                                                }
                                                Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Open", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                                            }
                                        }
                                    }
                                } else {
                                    item {
                                        Row(
                                            modifier = Modifier.fillMaxWidth().clickable { selectedFolder = null }.padding(vertical = 8.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.primary)
                                            Spacer(modifier = Modifier.width(8.dp))
                                            Text("Back to Folders", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                    val folderItems = completedDownloads.filter { !it.isMovie && (it.title.split(" - ").firstOrNull() ?: it.title) == selectedFolder }
                                    items(folderItems) { item ->
                                        SendItemRow(item, context, p2pManager, connectedEndpoint) { 
                                            showSendDialog = false 
                                            selectedFolder = null
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    showSendDialog = false
                    selectedFolder = null
                    p2pManager.stopAll()
                }) { Text("Cancel") }
            }
        )
    }

    if (showReceiveDialog) {
        AlertDialog(
            onDismissRequest = {
                showReceiveDialog = false
                p2pManager.stopAll()
            },
            title = { Text("Receive Media", fontWeight = FontWeight.Bold) },
            text = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    if (connectedEndpoint != null) {
                        Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color.Green, modifier = Modifier.size(64.dp))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Connected to ${connectedEndpoint!!.name}", fontWeight = FontWeight.Bold)
                        Text("Waiting for files...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } else {
                        Box(
                            modifier = Modifier
                                .size(200.dp)
                                .background(Color.White, RoundedCornerShape(16.dp))
                                .padding(16.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Outlined.QrCode2, contentDescription = "QR Code", tint = Color.Black, modifier = Modifier.fillMaxSize())
                        }
                        Spacer(modifier = Modifier.height(24.dp))
                        CircularProgressIndicator(modifier = Modifier.size(24.dp), strokeWidth = 2.dp)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Ready to receive", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text("Make sure the sender is on the same Wi-Fi network or Bluetooth is enabled. Transfer uses high-speed Wi-Fi Direct.", textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, modifier = Modifier.padding(horizontal = 16.dp))
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    showReceiveDialog = false
                    p2pManager.stopAll()
                }) { Text("Cancel") }
            }
        )
    }
}

@Composable
fun RowScope.ContentTypeCard(title: String, icon: ImageVector, isSelected: Boolean, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .weight(1f)
            .aspectRatio(1f)
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF19191C)),
        shape = RoundedCornerShape(12.dp),
        border = if (isSelected) BorderStroke(1.dp, Color.Red) else null
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(icon, contentDescription = title, tint = if (isSelected) Color.Red else Color.Gray, modifier = Modifier.size(28.dp))
            Spacer(modifier = Modifier.height(8.dp))
            Text(title, color = if (isSelected) Color.Red else Color.Gray, fontSize = 11.sp, textAlign = TextAlign.Center)
        }
    }
}

@Composable
fun RecentTransferItem(title: String, type: String, size: String, isSent: Boolean, time: String, targetDevice: String, isCompleted: Boolean) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Thumbnail placeholder
        Box(
            modifier = Modifier
                .size(60.dp)
                .clip(RoundedCornerShape(8.dp))
                .background(Color(0xFF2A2A2E)),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Outlined.Movie, contentDescription = null, tint = Color.Gray)
        }
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("$type • $size", color = Color.Gray, fontSize = 11.sp)
                Spacer(modifier = Modifier.width(8.dp))
                Icon(
                    if (isSent) Icons.Default.ArrowUpward else Icons.Default.ArrowDownward,
                    contentDescription = null,
                    tint = if (isSent) Color.Red else Color(0xFF3b82f6),
                    modifier = Modifier.size(12.dp)
                )
                Spacer(modifier = Modifier.width(2.dp))
                Text(if (isSent) "Sent" else "Received", color = if (isSent) Color.Red else Color(0xFF3b82f6), fontSize = 11.sp)
            }
            Text(if (isSent) "To: $targetDevice" else "From: $targetDevice", color = Color.Gray, fontSize = 11.sp)
        }
        
        Column(horizontalAlignment = Alignment.End) {
            Text(time, color = Color.Gray, fontSize = 11.sp)
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.CheckCircleOutline, contentDescription = null, tint = Color(0xFF10b981), modifier = Modifier.size(14.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text("Completed", color = Color(0xFF10b981), fontSize = 11.sp)
            }
        }
    }
}

@Composable
fun NearbyDeviceItem(name: String, onConnect: () -> Unit = {}) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .background(Color(0xFF19191C))
                .border(1.dp, Color(0xFF2A2A2E), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.PhoneAndroid, contentDescription = null, tint = Color.Red, modifier = Modifier.size(20.dp))
        }
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(modifier = Modifier.weight(1f)) {
            Text(name, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            Text("Android • Ready to connect", color = Color.Gray, fontSize = 11.sp)
        }
        
        Icon(Icons.Default.SignalCellularAlt, contentDescription = "Signal", tint = Color(0xFF10b981), modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(16.dp))
        
        Button(
            onClick = onConnect,
            colors = ButtonDefaults.buttonColors(containerColor = Color.Red.copy(alpha = 0.2f), contentColor = Color.Red),
            shape = RoundedCornerShape(8.dp),
            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
            modifier = Modifier.height(32.dp)
        ) {
            Text("Connect", fontSize = 12.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun SendItemRow(item: DownloadItem, context: android.content.Context, p2pManager: P2PManager, connectedEndpoint: Endpoint?, onSent: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable {
                val file = File(context.filesDir, "downloads/${item.id}.mp4")
                if (file.exists() && connectedEndpoint != null) {
                    p2pManager.sendMovie(connectedEndpoint.id, item.id, item.title, item.isMovie, item.posterUrl, file)
                }
                onSent()
            }
            .padding(vertical = 12.dp, horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(Icons.Outlined.Movie, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.width(16.dp))
        Column {
            Text(item.title, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
            Text(if (item.isMovie) "Movie" else "Episode", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
        }
        Spacer(modifier = Modifier.weight(1f))
        Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
    }
}

