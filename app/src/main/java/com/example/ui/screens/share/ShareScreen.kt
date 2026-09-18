package com.example.ui.screens.share

import androidx.compose.ui.res.stringResource
import com.example.ui.theme.SuccessGreen
import com.example.R

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
    onBack: () -> Unit,
    onItemClick: (String, Boolean) -> Unit = { _, _ -> }
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var transitionFinished by remember { androidx.compose.runtime.mutableStateOf(false) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(1200)
        transitionFinished = true
    }
    if (!transitionFinished) {
        com.example.ui.components.ShareScreenSkeleton()
        return
    }

    val p2pManager = remember { P2PManager(context) }
    val downloadRepository = remember { com.example.data.repository.DownloadRepository(context) }
    
    val p2pState by p2pManager.p2pState.collectAsState()
    val connectedEndpoint by p2pManager.connectedEndpoint.collectAsState()
    val discoveredEndpoints by p2pManager.discoveredEndpoints.collectAsState()
    val transferProgress by p2pManager.transferProgress.collectAsState()
    
    val allDownloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val completedDownloads = remember(allDownloads) { allDownloads.filter { it.isCompleted } }

    DisposableEffect(Unit) {
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

    Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 16.dp),
            contentPadding = PaddingValues(top = 16.dp, bottom = 24.dp)
        ) {
            // Connection Status Card
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
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
                                .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.3f), CircleShape)
                                .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.WifiTethering, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                        }
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        Column(modifier = Modifier.weight(1f)) {
                            Text(stringResource(R.string.connection_status), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                            val statusText = when (p2pState) {
                                P2PState.DISCOVERING -> "DISCOVERING"
                                P2PState.ADVERTISING -> "ADVERTISING"
                                P2PState.CONNECTED -> "CONNECTED"
                                P2PState.TRANSFERRING -> "TRANSFERRING"
                                else -> "IDLE"
                            }
                            Text(statusText, color = MaterialTheme.colorScheme.primary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                            Text(stringResource(R.string.waiting_for_action), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                        }
                        
                        OutlinedButton(
                            onClick = { /* How it works */ },
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = MaterialTheme.colorScheme.onBackground),
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)),
                            shape = RoundedCornerShape(20.dp),
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Text(stringResource(R.string.how_it_works), fontSize = 12.sp)
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
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primary),
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
                                    .background(MaterialTheme.colorScheme.onBackground.copy(alpha = 0.2f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.AutoMirrored.Filled.Send, contentDescription = stringResource(R.string.send), tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(20.dp))
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(stringResource(R.string.send_content), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                Text(stringResource(R.string.share_desc), color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.8f), fontSize = 11.sp, lineHeight = 14.sp)
                            }
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(16.dp))
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
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
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
                                    .background(MaterialTheme.colorScheme.onBackground.copy(alpha = 0.1f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Download, contentDescription = stringResource(R.string.receive), tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(20.dp))
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(stringResource(R.string.receive_content), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                Text(stringResource(R.string.receive_from_nearby), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp, lineHeight = 14.sp)
                            }
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(16.dp))
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Content Type Selector
            item {
                Text(stringResource(R.string.choose_content_type), color = MaterialTheme.colorScheme.onBackground, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(12.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    ContentTypeCard(stringResource(R.string.category_movies), Icons.Outlined.Movie, selectedContentType == "Movies") { selectedContentType = "Movies" }
                    ContentTypeCard(stringResource(R.string.category_series), Icons.Outlined.Tv, selectedContentType == "TV Series") { selectedContentType = "TV Series" }
                    ContentTypeCard(stringResource(R.string.category_anime), Icons.Default.Face, selectedContentType == "Anime") { selectedContentType = "Anime" }
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
                    Text(stringResource(R.string.recent_transfers), color = MaterialTheme.colorScheme.onBackground, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Text(stringResource(R.string.view_all), color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                }
                Spacer(modifier = Modifier.height(12.dp))
                
                val recentItems = completedDownloads.reversed().take(3)
                if (recentItems.isEmpty()) {
                    Text(stringResource(R.string.no_downloads), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                } else {
                    recentItems.forEachIndexed { index, item ->
                        RecentTransferItem(
                            item = item,
                            onClick = { onItemClick(item.mediaId, item.isMovie) }
                        )
                        if (index < recentItems.size - 1) {
                            HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(vertical = 12.dp))
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Nearby Devices List
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(stringResource(R.string.nearby_devices), color = MaterialTheme.colorScheme.onBackground, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable { p2pManager.startDiscovery() }) {
                        Icon(Icons.Default.Refresh, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(14.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(stringResource(R.string.scan), color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                    }
                }
                Spacer(modifier = Modifier.height(12.dp))
                
                if (discoveredEndpoints.isEmpty()) {
                    // Demo devices based on screenshot
                    NearbyDeviceItem("Ahmed's Phone")
                    HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(vertical = 12.dp))
                    NearbyDeviceItem("Sara's Phone")
                } else {
                    discoveredEndpoints.forEachIndexed { index, endpoint ->
                        NearbyDeviceItem(endpoint.name) {
                            p2pManager.requestConnection(endpoint.id, Build.MODEL)
                        }
                        if (index < discoveredEndpoints.size - 1) {
                            HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(vertical = 12.dp))
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
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Row(modifier = Modifier.padding(16.dp)) {
                        Box(
                            modifier = Modifier.size(32.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Outlined.Shield, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(stringResource(R.string.tips_faster_transfer), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(stringResource(R.string.share_instruction_1), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, lineHeight = 18.sp)
                        }
                    }
                }
            }
        }
    }

    var selectedFolder by remember { mutableStateOf<String?>(null) }
    var selectedItemsToSend by remember { mutableStateOf<Set<DownloadItem>>(emptySet()) }
    
    // Kept the functional dialogs unchanged logic-wise, but using the dark theme
    if (showSendDialog) {
        AlertDialog(
            onDismissRequest = {
                showSendDialog = false
                selectedFolder = null
                selectedItemsToSend = emptySet()
                p2pManager.stopAll()
            },
            title = { Text(if (selectedFolder == null) "Select Media to Send" else selectedFolder!!, fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    if (p2pState == P2PState.DISCOVERING && discoveredEndpoints.isEmpty()) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally).padding(16.dp))
                        Text(stringResource(R.string.looking_for_devices), textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
                    } else if (discoveredEndpoints.isNotEmpty() && connectedEndpoint == null) {
                        Text(stringResource(R.string.available_devices), fontWeight = FontWeight.Bold, modifier = Modifier.padding(vertical = 8.dp))
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
                        Text(stringResource(R.string.connected_to, connectedEndpoint?.name ?: ""), color = SuccessGreen, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp)) {
                            if (completedDownloads.isEmpty()) {
                                item { Text(stringResource(R.string.no_downloads), color = MaterialTheme.colorScheme.onSurfaceVariant) }
                            } else {
                                if (selectedFolder == null) {
                                    val movies = completedDownloads.filter { it.isMovie }
                                    val series = completedDownloads.filter { !it.isMovie }
                                    
                                    if (movies.isNotEmpty()) {
                                        item { Text(stringResource(R.string.movies), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                        items(movies) { item ->
                                            val isSelected = selectedItemsToSend.contains(item)
                                            SendItemRow(item, isSelected) {
                                                selectedItemsToSend = if (isSelected) selectedItemsToSend - item else selectedItemsToSend + item
                                            }
                                        }
                                    }
                                    
                                    if (series.isNotEmpty()) {
                                        item { Text(stringResource(R.string.series_anime), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(vertical = 8.dp)) }
                                        val groupedSeries = series.groupBy { it.title.split(" - ").firstOrNull() ?: it.title }
                                        items(groupedSeries.keys.toList()) { folderName ->
                                            Row(
                                                modifier = Modifier
                                                    .fillMaxWidth()
                                                    .clickable { selectedFolder = folderName }
                                                    .padding(vertical = 12.dp, horizontal = 8.dp),
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                Icon(Icons.Outlined.Folder, contentDescription = stringResource(R.string.folder), tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                                                Spacer(modifier = Modifier.width(16.dp))
                                                Column(modifier = Modifier.weight(1f)) {
                                                    Text(folderName, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                                    Text(stringResource(R.string.episodes_count, groupedSeries[folderName]?.size ?: 0), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                                                }
                                                Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = stringResource(R.string.open), tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                                            }
                                        }
                                    }
                                } else {
                                    item {
                                        Row(
                                            modifier = Modifier.fillMaxWidth().clickable { selectedFolder = null }.padding(vertical = 8.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back), tint = MaterialTheme.colorScheme.primary)
                                            Spacer(modifier = Modifier.width(8.dp))
                                            Text(stringResource(R.string.back_to_folders), color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
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
                        p2pManager.stopAll()
                    }) { Text(stringResource(R.string.cancel)) }
                    
                    if (connectedEndpoint != null && selectedItemsToSend.isNotEmpty()) {
                        Button(onClick = {
                            selectedItemsToSend.forEach { item ->
                                val file = File(context.filesDir, "downloads/${item.id}.mp4")
                                if (file.exists()) {
                                    p2pManager.sendMedia(connectedEndpoint!!.id, item, file)
                                }
                            }
                            showSendDialog = false
                            selectedFolder = null
                            selectedItemsToSend = emptySet()
                        }) {
                            Text("Send (${selectedItemsToSend.size})")
                        }
                    }
                }
            }
        )
    }

    if (showReceiveDialog) {
        AlertDialog(
            onDismissRequest = {
                showReceiveDialog = false
                p2pManager.stopAll()
            },
            title = { Text(stringResource(R.string.receive_media), fontWeight = FontWeight.Bold) },
            text = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    if (connectedEndpoint != null) {
                        Icon(Icons.Default.CheckCircle, contentDescription = null, tint = SuccessGreen, modifier = Modifier.size(64.dp))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(stringResource(R.string.connected_to, connectedEndpoint!!.name), fontWeight = FontWeight.Bold)
                        Text(stringResource(R.string.waiting_for_files), color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } else {
                        Box(
                            modifier = Modifier
                                .size(200.dp)
                                .background(MaterialTheme.colorScheme.onBackground, RoundedCornerShape(16.dp))
                                .padding(16.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Outlined.QrCode2, contentDescription = stringResource(R.string.qr_code), tint = MaterialTheme.colorScheme.background, modifier = Modifier.fillMaxSize())
                        }
                        Spacer(modifier = Modifier.height(24.dp))
                        CircularProgressIndicator(modifier = Modifier.size(24.dp), strokeWidth = 2.dp)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(stringResource(R.string.ready_to_receive), fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text(stringResource(R.string.share_instruction_2), textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, modifier = Modifier.padding(horizontal = 16.dp))
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    showReceiveDialog = false
                    p2pManager.stopAll()
                }) { Text(stringResource(R.string.cancel)) }
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
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        shape = RoundedCornerShape(12.dp),
        border = if (isSelected) BorderStroke(1.dp, MaterialTheme.colorScheme.primary) else null
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(icon, contentDescription = title, tint = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(28.dp))
            Spacer(modifier = Modifier.height(8.dp))
            Text(title, color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp, textAlign = TextAlign.Center)
    }
}
}

@Composable
fun RecentTransferItem(item: DownloadItem, onClick: () -> Unit) {
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
            Text(item.title, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(if (item.isMovie) "Movie" else "Episode", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp)
                Spacer(modifier = Modifier.width(8.dp))
                Icon(
                    Icons.Default.ArrowDownward,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.secondary,
                    modifier = Modifier.size(12.dp)
                )
                Spacer(modifier = Modifier.width(2.dp))
                Text(stringResource(R.string.received), color = MaterialTheme.colorScheme.secondary, fontSize = 11.sp)
            }
        }
        
        Column(horizontalAlignment = Alignment.End) {
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.CheckCircleOutline, contentDescription = null, tint = SuccessGreen, modifier = Modifier.size(14.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(stringResource(R.string.completed), color = SuccessGreen, fontSize = 11.sp)
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
                .background(MaterialTheme.colorScheme.surface)
                .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.PhoneAndroid, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
        }
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(modifier = Modifier.weight(1f)) {
            Text(name, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            Text(stringResource(R.string.android_ready), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 11.sp)
        }
        
        Icon(Icons.Default.SignalCellularAlt, contentDescription = stringResource(R.string.signal), tint = SuccessGreen, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(16.dp))
        
        Button(
            onClick = onConnect,
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f), contentColor = MaterialTheme.colorScheme.primary),
            shape = RoundedCornerShape(8.dp),
            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
            modifier = Modifier.height(32.dp)
        ) {
            Text(stringResource(R.string.connect), fontSize = 12.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun SendItemRow(item: DownloadItem, isSelected: Boolean, onSelect: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onSelect() }
            .padding(vertical = 12.dp, horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(Icons.Outlined.Movie, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(item.title, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
            Text(if (item.isMovie) "Movie" else "Episode", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
        }
        Checkbox(
            checked = isSelected,
            onCheckedChange = { onSelect() }
        )
    }    
}

