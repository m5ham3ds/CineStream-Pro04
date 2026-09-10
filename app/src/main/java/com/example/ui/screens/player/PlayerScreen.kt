package com.example.ui.screens.player

import android.app.Activity
import android.content.pm.ActivityInfo
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.CookieManager
import androidx.annotation.OptIn
import androidx.compose.animation.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.List
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.datasource.DefaultHttpDataSource
import androidx.media3.exoplayer.source.DefaultMediaSourceFactory

import androidx.core.view.WindowInsetsControllerCompat
import androidx.core.view.WindowInsetsCompat
import androidx.media3.exoplayer.trackselection.DefaultTrackSelector

import androidx.compose.ui.unit.sp
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Speed
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.VideoLibrary
import androidx.compose.material.icons.filled.Replay10
import androidx.compose.material.icons.filled.Forward10
import kotlinx.coroutines.delay
import androidx.media3.ui.PlayerView
import com.example.ui.components.DownloadQualitySheet

@OptIn(androidx.media3.common.util.UnstableApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
@Suppress("OPT_IN_USAGE")
fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, url: String? = null, targetServer: String? = null, website: String? = null, onBack: () -> Unit, viewModel: PlayerViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(mediaId) {
        viewModel.initialize(mediaId, isMovie, title, url, targetServer, website)
    }

    val context = LocalContext.current
    var showDownloadSheet by remember { mutableStateOf(false) }
    var showControls by remember { mutableStateOf(true) }
    var isPlaying by remember { mutableStateOf(false) }
    var currentTime by remember { mutableStateOf(0L) }
    var totalDuration by remember { mutableStateOf(0L) }
    var brightness by remember { mutableStateOf(0.5f) }
    var volume by remember { mutableStateOf(0.5f) }
    var isLocked by remember { mutableStateOf(false) }
    var currentSpeed by remember { mutableStateOf(1f) }
    var currentQuality by remember { mutableStateOf("Auto") }
    var showQualitySheet by remember { mutableStateOf(false) }
    var showEpisodesSheet by remember { mutableStateOf(false) }
    
    // Server & Website state
    var showServerSheet by remember { mutableStateOf(false) }
    var showWebsiteSheet by remember { mutableStateOf(false) }
    var isCloudflareChallenge by remember { mutableStateOf(false) }

    // Force landscape mode for better viewing
    DisposableEffect(Unit) {
        val activity = context as? Activity
        activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
        
        val window = activity?.window
        var insetsController: WindowInsetsControllerCompat? = null
        if (window != null) {
            insetsController = WindowInsetsControllerCompat(window, window.decorView)
            insetsController.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            insetsController.hide(androidx.core.view.WindowInsetsCompat.Type.systemBars())
        }
        
        onDispose {
            activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
            insetsController?.show(androidx.core.view.WindowInsetsCompat.Type.systemBars())
        }
    }

    val trackSelector = remember { DefaultTrackSelector(context) }

    val exoPlayer = remember {
        // Build ExoPlayer with cookies from WebView
        val cookie = android.webkit.CookieManager.getInstance().getCookie(uiState.currentVideoUrl ?: "") ?: ""
        val dataSourceFactory = DefaultHttpDataSource.Factory()
            .setUserAgent("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
        if (cookie.isNotEmpty()) {
            dataSourceFactory.setDefaultRequestProperties(mapOf("Cookie" to cookie))
        }
        val mediaSourceFactory = DefaultMediaSourceFactory(dataSourceFactory)
        
        ExoPlayer.Builder(context)
            .setMediaSourceFactory(mediaSourceFactory)
            .setTrackSelector(trackSelector)
            .build().apply {
            addListener(object : Player.Listener {
                override fun onIsPlayingChanged(isPlayingChanged: Boolean) {
                    isPlaying = isPlayingChanged
                }
                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_READY) {
                        totalDuration = duration.coerceAtLeast(0L)
                    }
                }
            })
        }
    }
    
    LaunchedEffect(currentQuality) {
        val parametersBuilder = trackSelector.buildUponParameters()
        if (currentQuality == "Auto") {
            parametersBuilder.clearVideoSizeConstraints()
        } else {
            val height = currentQuality.replace("p", "").toIntOrNull()
            if (height != null) {
                // To force a specific quality, we set max and min to the same height,
                // or just max and clear others, but ExoPlayer usually respects max size constraints well.
                // We will set both max and min video size to force this exact resolution if available.
                parametersBuilder.setMaxVideoSize(Int.MAX_VALUE, height)
                parametersBuilder.setMinVideoSize(0, height)
            } else {
                parametersBuilder.clearVideoSizeConstraints()
            }
        }
        trackSelector.setParameters(parametersBuilder)
    }

    var showInitialSelection by remember { mutableStateOf(false) }

    // State to hold actual available qualities from ExoPlayer
    var availableVideoQualities by remember { mutableStateOf<List<String>>(listOf("Auto")) }


    LaunchedEffect(uiState.currentVideoUrl) {
        uiState.currentVideoUrl?.let { url ->
            // We need to recreate the media source if the url changes to ensure new cookies are fetched
            val cookie = android.webkit.CookieManager.getInstance().getCookie(url) ?: ""
            val dataSourceFactory = DefaultHttpDataSource.Factory()
                .setUserAgent("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
            if (cookie.isNotEmpty()) {
                dataSourceFactory.setDefaultRequestProperties(mapOf("Cookie" to cookie))
            }
            val mediaSource = DefaultMediaSourceFactory(dataSourceFactory).createMediaSource(MediaItem.fromUri(url))
            
            exoPlayer.setMediaSource(mediaSource)
            exoPlayer.prepare()
            if (!showInitialSelection) {
                exoPlayer.playWhenReady = true
            } else {
                exoPlayer.playWhenReady = false
            }
        }
    }

    LaunchedEffect(brightness) {
        val window = (context as? Activity)?.window
        window?.let {
            val lp = it.attributes
            lp.screenBrightness = brightness
            it.attributes = lp
        }
    }
    
    LaunchedEffect(volume) {
        exoPlayer.volume = volume
    }
    
    LaunchedEffect(isPlaying) {
        while (isPlaying) {
            currentTime = exoPlayer.currentPosition
            delay(1000)
        }
    }

    LaunchedEffect(showControls, isPlaying) {
        if (showControls && isPlaying) {
            delay(4000)
            if (!isLocked) showControls = false
        }
    }

    DisposableEffect(Unit) {
        onDispose {
            exoPlayer.release()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null
            ) {
                showControls = !showControls
            }
    ) {
        if (uiState.currentVideoUrl != null) {
            val videoUrl = uiState.currentVideoUrl!!
            val isDirectVideo = videoUrl.endsWith(".m3u8") || videoUrl.endsWith(".mp4") || videoUrl.endsWith(".mkv") || videoUrl.contains("videodelivery.net") || videoUrl.contains("v.mp4") || videoUrl.contains("v2.hyperwatching.com") == false && videoUrl.contains("play.vidyard.com") == false && videoUrl.contains(".html") == false && videoUrl.contains("iframe") == false && videoUrl.contains("embed") == false
            
            if (isDirectVideo && uiState.currentVideoUrl?.contains("embed") != true && uiState.currentVideoUrl?.contains("iframe") != true) {
                AndroidView(
                    factory = { ctx ->
                        PlayerView(ctx).apply {
                            player = exoPlayer
                            useController = false
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )
            } else {
                AndroidView(
                    factory = { ctx ->
                        WebView(ctx).apply {
                            settings.apply {
                                javaScriptEnabled = true
                                domStorageEnabled = true
                                mediaPlaybackRequiresUserGesture = false
                                useWideViewPort = true
                                loadWithOverviewMode = true
                                setSupportZoom(true)
                                builtInZoomControls = true
                                displayZoomControls = false
                                val originalUserAgent = WebSettings.getDefaultUserAgent(ctx)
                                userAgentString = originalUserAgent.replace("; wv", "").replace("Version/4.0 ", "")
                            }
                            val cookieManager = CookieManager.getInstance()
                            cookieManager.setAcceptCookie(true)
                            cookieManager.setAcceptThirdPartyCookies(this, true)
                            webViewClient = WebViewClient()
                            loadUrl(videoUrl)
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
        
        // Only load the webview when we don't have a video URL to save data and prevent double-loading
        if (uiState.currentVideoUrl == null) {
            uiState.extractionUrl?.let { url ->
                HiddenVideoExtractor(
                    url = url,
                    isMovie = uiState.isMovie,
                    season = uiState.currentSeasonNumber,
                    episode = uiState.currentEpisodeNumber,
                    targetServer = uiState.currentServer.ifEmpty { null },
                    targetServerId = uiState.serverIdToChange,
                    website = uiState.currentWebsite, title = uiState.title,
                    onVideoUrlFound = { extractedUrl ->
                        viewModel.setFinalVideoUrl(extractedUrl)
                    },
                    onIframeUrlFound = { iframeUrl ->
                        viewModel.setIframeUrl(iframeUrl)
                    },
                    onServersFound = { servers ->
                        viewModel.updateServers(servers)
                    },
                    onExtractionFailed = {
                        viewModel.tryNextFallback()
                    },
                    onCloudflareDetected = { isCf ->
                        isCloudflareChallenge = isCf
                    }
                )
            }
        }
        
        if (uiState.isLoading && !showInitialSelection && !isCloudflareChallenge) {
            Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.5f)), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    CircularProgressIndicator(color = Color(0xFFE50914))
                    Spacer(modifier = Modifier.height(16.dp))
                    val serverText = if (uiState.currentServer.isNotEmpty()) " / ${uiState.currentServer}" else ""
                    Text("Connecting to ${uiState.currentWebsite}$serverText...", color = Color.White)
                }
            }
        }

        AnimatedVisibility(
            visible = !showControls && !uiState.isLoading,
            enter = fadeIn(),
            exit = fadeOut(),
            modifier = Modifier.align(Alignment.TopCenter).fillMaxWidth()
        ) {
            Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxWidth()) {
                com.example.ui.components.StartAppBanner()
            }
        }

        AnimatedVisibility(
            visible = showControls,
            enter = fadeIn(),
            exit = fadeOut(),
            modifier = Modifier.fillMaxSize()
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.5f))
            ) {
                if (isLocked) {
                    // Only show unlock button if locked
                    IconButton(
                        onClick = { isLocked = false; showControls = true },
                        modifier = Modifier
                            .align(Alignment.CenterStart)
                            .padding(32.dp)
                    ) {
                        Icon(Icons.Default.Lock, contentDescription = "Unlock", tint = Color.White, modifier = Modifier.size(32.dp))
                    }
                } else {
                    // Top Bar
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 16.dp, start = 24.dp, end = 24.dp)
                            .align(Alignment.TopCenter),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        // Left section
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                            Icon(
                                Icons.AutoMirrored.Filled.ArrowBack, 
                                contentDescription = "Back", 
                                tint = Color.White, 
                                modifier = Modifier.size(28.dp).clickable { onBack() }
                            )
                            Spacer(modifier = Modifier.weight(1f))
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.clickable { showServerSheet = true }.padding(8.dp)
                            ) {
                                val serverName = if (uiState.currentServer.isNotEmpty()) uiState.currentServer.uppercase() else "SERVER"
                                Text(serverName, color = Color.Gray, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                            }
                            Spacer(modifier = Modifier.weight(1f))
                        }
                        
                        // Center section
                        Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.weight(1.2f)) {
                            Text(if(uiState.isMovie) "Movie" else "Series", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(uiState.title, color = Color.LightGray, fontSize = 14.sp)
                        }
                        
                        // Right section
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                            Spacer(modifier = Modifier.weight(1f))
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.clickable { showWebsiteSheet = true }.padding(8.dp)
                            ) {
                                Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Color(0xFFE50914), modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(uiState.currentWebsite.uppercase(), color = Color.Gray, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                            }
                            Spacer(modifier = Modifier.weight(1f))
                            Icon(
                                Icons.Default.MoreVert, 
                                contentDescription = "Menu", 
                                tint = Color.White, 
                                modifier = Modifier.size(28.dp).clickable { /* Menu */ }
                            )
                        }
                    }

                    // Left Vertical Slider (Brightness)
                    Box(modifier = Modifier.align(Alignment.CenterStart).padding(start = 24.dp)) {
                        VerticalSlider(
                            value = brightness, 
                            onValueChange = { brightness = it }
                        )
                    }

                    // Right Vertical Slider (Volume)
                    Box(modifier = Modifier.align(Alignment.CenterEnd).padding(end = 24.dp)) {
                        VerticalSlider(
                            value = volume, 
                            onValueChange = { volume = it }
                        )
                    }

                    // Center Playback Controls
                    if (uiState.currentVideoUrl == null) {
                        Column(
                            modifier = Modifier.align(Alignment.Center),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            CircularProgressIndicator(color = Color(0xFFE50914))
                            Spacer(modifier = Modifier.height(16.dp))
                            val serverText = if (uiState.currentServer.isNotEmpty()) " / ${uiState.currentServer}" else ""
                            Text("Loading ${uiState.currentWebsite}$serverText...", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    } else {
                        Row(
                            modifier = Modifier.align(Alignment.Center),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(32.dp)
                        ) {
                            Box(
                                contentAlignment = Alignment.Center,
                                modifier = Modifier
                                    .size(56.dp)
                                    .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                                    .clickable { exoPlayer.seekTo((exoPlayer.currentPosition - 10000).coerceAtLeast(0)) }
                            ) {
                                Icon(Icons.Default.Replay10, contentDescription = "Rewind", tint = Color.White, modifier = Modifier.size(28.dp))
                            }
                            
                            Box(
                                contentAlignment = Alignment.Center,
                                modifier = Modifier
                                    .size(72.dp)
                                    .border(2.dp, Color(0xFFE50914), CircleShape)
                                    .clickable { if (isPlaying) exoPlayer.pause() else exoPlayer.play() }
                            ) {
                                Icon(
                                    if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                                    contentDescription = "Play/Pause",
                                    tint = Color.White,
                                    modifier = Modifier.size(36.dp)
                                )
                            }
                            
                            Box(
                                contentAlignment = Alignment.Center,
                                modifier = Modifier
                                    .size(56.dp)
                                    .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                                    .clickable { exoPlayer.seekTo((exoPlayer.currentPosition + 10000).coerceAtMost(exoPlayer.duration)) }
                            ) {
                                Icon(Icons.Default.Forward10, contentDescription = "Forward", tint = Color.White, modifier = Modifier.size(28.dp))
                            }
                        }
                    }

                    // Bottom Controls
                    Column(
                        modifier = Modifier
                            .align(Alignment.BottomCenter)
                            .fillMaxWidth()
                            .padding(horizontal = 32.dp, vertical = 24.dp)
                    ) {
                        // Progress Bar Row
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text(formatTime(currentTime), color = Color.White, fontSize = 14.sp)
                            Spacer(modifier = Modifier.width(16.dp))
                            SimpleSlider(
                                value = if (totalDuration > 0) (currentTime.toFloat() / totalDuration.toFloat()) else 0f,
                                onValueChange = { percent ->
                                    val newPosition = (percent * totalDuration).toLong()
                                    exoPlayer.seekTo(newPosition)
                                    currentTime = newPosition
                                },
                                modifier = Modifier.weight(1f)
                            )
                            Spacer(modifier = Modifier.width(16.dp))
                            Text(formatTime(totalDuration), color = Color.White, fontSize = 14.sp)
                        }

                        Spacer(modifier = Modifier.height(16.dp))

                        // Action Toolbar Row
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            BottomAction(icon = Icons.Default.Speed, text = "Speed (${if (currentSpeed == 1f) "1" else currentSpeed}x)") { 
                                val nextSpeed = when(currentSpeed) {
                                    0.5f -> 1f
                                    1f -> 1.5f
                                    1.5f -> 2f
                                    else -> 0.5f
                                }
                                currentSpeed = nextSpeed
                                exoPlayer.setPlaybackSpeed(nextSpeed)
                            }
                            ActionDivider()
                            BottomAction(icon = Icons.Default.Lock, text = "Lock") { isLocked = true }
                            ActionDivider()
                            if (!uiState.isMovie) { BottomAction(icon = Icons.Default.VideoLibrary, text = "Episodes") { showEpisodesSheet = true } }
                            ActionDivider()
                            QualityAction(uiState.currentQuality, onClick = { showQualitySheet = true })
                            ActionDivider()
                            BottomAction(icon = Icons.Default.Download, text = "Download") { showDownloadSheet = true }
                        }
                    }
                }
            }
        }
    }

    // Modal Bottom Sheets
    if (showQualitySheet) {
        ModalBottomSheet(
            onDismissRequest = { showQualitySheet = false },
            containerColor = Color(0xFF1C1C1E)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Select Quality", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                availableVideoQualities.forEach { q ->
                    TextButton(
                        onClick = { 
                            currentQuality = q
                            showQualitySheet = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(q, color = if (q == currentQuality) Color(0xFFE50914) else Color.White)
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
    
    if (showEpisodesSheet) {
        ModalBottomSheet(
            onDismissRequest = { showEpisodesSheet = false },
            containerColor = Color(0xFF1C1C1E)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Episodes", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                LazyColumn {
                    items(uiState.episodes) { ep ->
                        TextButton(
                            onClick = { 
                                viewModel.selectEpisode(ep)
                                showEpisodesSheet = false 
                            },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text(
                                "Episode ${ep.episodeNumber}: ${ep.title}", 
                                color = if (ep.id == uiState.currentEpisodeId) Color(0xFFE50914) else Color.White
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }

    if (showServerSheet) {
        ModalBottomSheet(
            onDismissRequest = { showServerSheet = false },
            containerColor = Color(0xFF1C1C1E)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Select Server", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                uiState.availableServers.forEach { s ->
                    TextButton(
                        onClick = { 
                            viewModel.selectServer(s)
                            showServerSheet = false
                            android.widget.Toast.makeText(context, "Switched to $s", android.widget.Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(s, color = if (s == uiState.currentServer) Color(0xFFE50914) else Color.White)
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }

    if (showWebsiteSheet) {
        ModalBottomSheet(
            onDismissRequest = { showWebsiteSheet = false },
            containerColor = Color(0xFF1C1C1E)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Select Source Website", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                uiState.availableWebsites.forEach { w ->
                    TextButton(
                        onClick = { 
                            viewModel.selectWebsite(w)
                            showWebsiteSheet = false
                            android.widget.Toast.makeText(context, "Switched source to $w", android.widget.Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(w, color = if (w == uiState.currentWebsite) Color(0xFFE50914) else Color.White)
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }

    if (showDownloadSheet) {
        DownloadQualitySheet(
            qualities = availableVideoQualities.filter { it != "Auto" }.ifEmpty { listOf("Default") },
            onDismiss = { showDownloadSheet = false },
            onQualitySelected = { quality ->
                uiState.currentVideoUrl?.let { videoUrl ->
                    com.example.utils.AndroidDownloader.downloadVideo(context, videoUrl, "${uiState.title} - $quality")
                } ?: run {
                    android.widget.Toast.makeText(context, "Please wait for the stream to load first.", android.widget.Toast.LENGTH_SHORT).show()
                }
                showDownloadSheet = false
            }
        )
    }

    if (showInitialSelection) {
        androidx.compose.ui.window.Dialog(onDismissRequest = { 
            // Do not dismiss on outside click to force selection or back press
            onBack()
        }, properties = androidx.compose.ui.window.DialogProperties(dismissOnBackPress = true, dismissOnClickOutside = false)) {
            androidx.compose.material3.Card(
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                colors = androidx.compose.material3.CardDefaults.cardColors(containerColor = Color(0xFF1C1C1E)),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp)
            ) {
                Column(modifier = Modifier.padding(24.dp).fillMaxWidth()) {
                    if (uiState.currentVideoUrl == null || uiState.isLoading) {
                        CircularProgressIndicator(color = Color(0xFFE50914), modifier = Modifier.align(Alignment.CenterHorizontally))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Searching for video...", color = Color.White, fontWeight = FontWeight.Bold, modifier = Modifier.align(Alignment.CenterHorizontally))
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Current Site: ${uiState.currentWebsite}", color = Color.Gray, fontSize = 14.sp, modifier = Modifier.align(Alignment.CenterHorizontally))
                    } else {
                        Text("Ready to Play", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Text("Source:", color = Color.Gray, fontSize = 14.sp)
                        Text(uiState.currentWebsite, color = Color(0xFFE50914), fontWeight = FontWeight.SemiBold)
                        
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Text("Quality:", color = Color.Gray, fontSize = 14.sp)
                        androidx.compose.foundation.lazy.LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            items(availableVideoQualities) { q ->
                                androidx.compose.material3.FilterChip(
                                    selected = (currentQuality == q),
                                    onClick = { currentQuality = q },
                                    label = { Text(q) },
                                    colors = androidx.compose.material3.FilterChipDefaults.filterChipColors(
                                        selectedContainerColor = Color(0xFFE50914),
                                        selectedLabelColor = Color.White
                                    )
                                )
                            }
                        }
                        
                        Spacer(modifier = Modifier.height(24.dp))
                        
                        Button(
                            onClick = { 
                                showInitialSelection = false
                                exoPlayer.playWhenReady = true
                                exoPlayer.play()
                            },
                            modifier = Modifier.fillMaxWidth(),
                            colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = null)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Play Now")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun VerticalSlider(
    value: Float,
    onValueChange: (Float) -> Unit
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Canvas(
            modifier = Modifier
                .width(32.dp)
                .height(140.dp)
                .pointerInput(Unit) {
                    detectTapGestures { offset ->
                        val newValue = 1f - (offset.y / size.height).coerceIn(0f, 1f)
                        onValueChange(newValue)
                    }
                }
                .pointerInput(Unit) {
                    detectDragGestures { change, _ ->
                        val newValue = 1f - (change.position.y / size.height).coerceIn(0f, 1f)
                        onValueChange(newValue)
                    }
                }
        ) {
            val width = size.width
            val height = size.height
            val centerX = width / 2f
            val trackWidth = 4.dp.toPx()
            val thumbRadius = 8.dp.toPx()
            
            val thumbY = height - (height * value)
            
            // Inactive Track (Full height)
            drawRoundRect(
                color = Color.White.copy(alpha = 0.3f),
                topLeft = Offset(centerX - trackWidth / 2f, 0f),
                size = Size(trackWidth, height),
                cornerRadius = CornerRadius(trackWidth / 2f)
            )
            
            // Active Track (From bottom to thumb)
            drawRoundRect(
                color = Color.White,
                topLeft = Offset(centerX - trackWidth / 2f, thumbY),
                size = Size(trackWidth, height - thumbY),
                cornerRadius = CornerRadius(trackWidth / 2f)
            )
            
            // Thumb
            drawCircle(
                color = Color.White,
                radius = thumbRadius,
                center = Offset(centerX, thumbY)
            )
        }
    }
}

@Composable
fun BottomAction(icon: ImageVector, text: String, onClick: () -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text(text, color = Color.LightGray, fontSize = 14.sp, fontWeight = FontWeight.Normal)
    }
}

@Composable
fun QualityAction(currentQuality: String, onClick: () -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(Icons.Default.Settings, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text("Quality", color = Color.LightGray, fontSize = 14.sp, fontWeight = FontWeight.Normal)
        Spacer(modifier = Modifier.width(6.dp))
        Box(
            modifier = Modifier
                .border(1.dp, Color(0xFFE50914), CircleShape)
                .padding(horizontal = 6.dp, vertical = 2.dp)
        ) {
            Text(currentQuality, color = Color(0xFFE50914), fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun ActionDivider() {
    Box(
        modifier = Modifier
            .width(1.dp)
            .height(16.dp)
            .background(Color.DarkGray)
    )
}

fun formatTime(timeMs: Long): String {
    if (timeMs < 0) return "00:00"
    val totalSeconds = timeMs / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    return String.format("%02d:%02d", minutes, seconds)
}

@Composable
fun SimpleSlider(
    value: Float,
    onValueChange: (Float) -> Unit,
    modifier: Modifier = Modifier,
    activeColor: Color = Color(0xFFE50914),
    inactiveColor: Color = Color.DarkGray,
    thumbColor: Color = Color(0xFFE50914),
    thumbRadius: Float = 12f,
    trackHeight: Float = 4f // Made track slightly thinner for elegance
) {
    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(32.dp) // Touch target height
            .pointerInput(Unit) {
                detectTapGestures { offset ->
                    onValueChange((offset.x / size.width).coerceIn(0f, 1f))
                }
            }
            .pointerInput(Unit) {
                detectDragGestures { change, _ ->
                    onValueChange((change.position.x / size.width).coerceIn(0f, 1f))
                }
            }
    ) {
        val width = size.width
        val height = size.height
        val centerY = height / 2f
        
        // Inactive Track
        drawRoundRect(
            color = inactiveColor,
            topLeft = Offset(0f, centerY - trackHeight / 2f),
            size = Size(width, trackHeight),
            cornerRadius = CornerRadius(trackHeight / 2f)
        )
        
        // Active Track
        drawRoundRect(
            color = activeColor,
            topLeft = Offset(0f, centerY - trackHeight / 2f),
            size = Size(width * value, trackHeight),
            cornerRadius = CornerRadius(trackHeight / 2f)
        )
        
        // Thumb
        drawCircle(
            color = thumbColor,
            radius = thumbRadius,
            center = Offset(width * value, centerY)
        )
    }
}
