package com.example.ui.screens.player
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.automirrored.outlined.ArrowBack

import androidx.compose.ui.res.stringResource
import com.example.R

import androidx.compose.animation.togetherWith

import com.example.extensions.ProviderExtension

import com.example.extensions.ExtensionManager
import androidx.compose.material.icons.filled.ArrowBack

import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.ui.zIndex
import androidx.compose.ui.unit.IntOffset

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.animation.animateContentSize

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.OpenInBrowser
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.outlined.CloudOff
import androidx.compose.material.icons.outlined.CloudDone
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Brush
import androidx.compose.foundation.border
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.draw.clip
import androidx.compose.material.icons.outlined.CloudDownload
import androidx.compose.material.icons.outlined.Security
import androidx.compose.material.icons.outlined.Sync
import androidx.compose.material.icons.outlined.Storage
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.sp
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.net.URLEncoder

@SuppressLint("SetJavaScriptEnabled")
@OptIn(ExperimentalMaterial3Api::class)

@Composable
fun ServerSelectionDialog(
    title: String,
    year: String = "",
    isMovie: Boolean,
    season: Int = 1,
    episode: Int = 1,
    isAnime: Boolean = false,
    isDownloadMode: Boolean = false,
    onDismiss: () -> Unit,
    onPlay: (url: String, serverName: String, website: String) -> Unit,
    onNavigateToExtensions: () -> Unit = {}
) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    
    
    val mediaKey = "$title-$isMovie-$season-$episode"

    val installedExtensions = ExtensionManager.installedExtensions.collectAsState().value
    val safeSites = if (installedExtensions.isNotEmpty()) installedExtensions else listOf(com.example.extensions.ExtensionReflectionWrapper(Any()))
    
    var currentSiteIndex by remember { mutableStateOf(0) }
    var currentExtension by remember { mutableStateOf(safeSites[0]) }
    val currentSiteName = currentExtension.name
    
    var isLoading by remember { mutableStateOf(ServerStateStore.currentMediaKey != mediaKey || ServerStateStore.extractedServers.isEmpty()) }
    var loadingMessage by remember { mutableStateOf("جاري الفحص وتخطي الحماية...") }
    
    var extractedServers by remember { mutableStateOf<List<String>>(
        if (ServerStateStore.currentMediaKey == mediaKey) ServerStateStore.extractedServers else emptyList()
    ) }
    var extractedServerLinks by remember { mutableStateOf<Map<String, String>>(
        if (ServerStateStore.currentMediaKey == mediaKey) ServerStateStore.extractedServerLinks else emptyMap()
    ) }
    var extractedServerIds by remember { mutableStateOf<Map<String, String>>(
        if (ServerStateStore.currentMediaKey == mediaKey) ServerStateStore.extractedServerIds else emptyMap()
    ) }
    var extractedDownloadLinks by remember { mutableStateOf<Map<String, String>>(
        if (ServerStateStore.currentMediaKey == mediaKey) ServerStateStore.extractedDownloadLinks else emptyMap()
    ) }
    var finalWatchUrl by remember { mutableStateOf<String?>(null) }
    var isFailed by remember { mutableStateOf(false) }
    var bypassStatus by remember { mutableStateOf(if (isLoading) "CHECKING_CLOUDFLARE" else "NORMAL") }
    var showCancelConfirmDialog by remember { mutableStateOf(false) }
    var isNetworkError by remember { mutableStateOf(false) }
    var retryTrigger by remember { mutableIntStateOf(0) }
    var showManualConfirmDialog by remember { mutableStateOf(false) }
    var showOpenBrowserConfirmDialog by remember { mutableStateOf(false) }
    var showSkipSiteConfirmDialog by remember { mutableStateOf(false) }
    var showNoMoreExtensionsDialog by remember { mutableStateOf(false) }
    var isManualBrowserOpen by remember { mutableStateOf(false) }
    var forceBypassComplete by remember { mutableStateOf(false) }

    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }

    // --- Quality Extraction States ---
    var selectedServerForQuality by remember { mutableStateOf<String?>(null) }
    var isExtractingQuality by remember { mutableStateOf(false) }
    var extractingEmbedUrl by remember { mutableStateOf<String?>(null) }
    var qualityExtractionMessage by remember { mutableStateOf("جاري استخراج الجودات المتاحة...") }
    var extractedQualities by remember { mutableStateOf<List<com.example.utils.M3U8Parser.QualityInfo>>(
        if (ServerStateStore.currentMediaKey == mediaKey) ServerStateStore.extractedQualities else emptyList()
    ) }

    LaunchedEffect(currentSiteIndex, retryTrigger) {
        if (!isLoading && extractedServers.isNotEmpty()) {
            return@LaunchedEffect
        }
        if (currentSiteIndex >= safeSites.size) {
            isLoading = false
            isFailed = true
            return@LaunchedEffect
        }
        
        currentExtension = safeSites[currentSiteIndex]
        bypassStatus = "CHECKING_CLOUDFLARE"
        forceBypassComplete = false
        loadingMessage = "جاري الفحص في موقع $currentSiteName..."
        extractedServers = emptyList()
        finalWatchUrl = null
        
        // Wait for up to 300 seconds (5 minutes) unconditionally
        var waited = 0
        while (waited < 300) {
            delay(1000)
            waited++
            if (extractedServers.isNotEmpty()) {
                // Servers found! We can stop waiting.
                return@LaunchedEffect
            }
            if (isFailed) {
                return@LaunchedEffect
            }
        }
        
        // If we timed out and still no servers, move to the next site
        if (extractedServers.isEmpty()) {
            currentSiteIndex++
        }
    }

    val baseTitle = if (title.contains(" - S") && title.contains("E")) {
        title.substringBefore(" - S").trim()
    } else {
        title
    }
    // نضيف سنة الإصدار للعنوان الأصلي إذا كانت موجودة لضمان دقة البحث بين الأجزاء
    val cleanTitleWithYear = if (year.isNotBlank() && year != "0") {
        "$baseTitle $year".replace(Regex("[^a-zA-Z0-9\\s]"), " ").replace(Regex("\\s+"), " ").trim()
    } else {
        baseTitle.replace(Regex("[^a-zA-Z0-9\\s]"), " ").replace(Regex("\\s+"), " ").trim()
    }
    
    val cleanTitle = baseTitle.replace(Regex("[^a-zA-Z0-9\\s]"), " ").replace(Regex("\\s+"), " ").trim()
    
    // Use cleanTitle for search so the site actually returns results (site search engines often fail with year appended)
    val searchUrl = currentExtension.getSearchUrl(baseTitle, cleanTitle)

Dialog(
        onDismissRequest = {
            if (isLoading) {
                showCancelConfirmDialog = true
            } else {
                onDismiss()
            }
        },
        properties = DialogProperties(
            usePlatformDefaultWidth = false,
            dismissOnClickOutside = false,
            dismissOnBackPress = true
        )
    ) {
        val isVerified = bypassStatus == "VERIFIED"
        val isNormal = bypassStatus == "NORMAL"
        val isCloudflare = bypassStatus == "CLOUDFLARE"

        val activeColor = if (isVerified || isNormal) Color(0xFF00C853) else Color(0xFFFF1111)


        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            
            // --- THE WEBVIEW (Draggable if Cloudflare, hidden otherwise) ---
            Box(
                modifier = if (isCloudflare) {
                    Modifier
                        .offset { androidx.compose.ui.unit.IntOffset(offsetX.toInt(), offsetY.toInt()) }
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                offsetX += dragAmount.x
                                offsetY += dragAmount.y
                            }
                        }
                        .fillMaxWidth(0.9f)
                        .fillMaxHeight(0.85f)
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.onBackground)
                        .zIndex(100f)
                } else {
                    Modifier.size(1.dp).alpha(0.01f).zIndex(-1f)
                }
            ) {
                Column(modifier = Modifier.fillMaxSize()) {
                    if (isCloudflare) {
                        Text(text = stringResource(R.string.skip_protect_prompt),
                            modifier = Modifier
                                .padding(16.dp)
                                .fillMaxWidth(),
                            textAlign = TextAlign.Center,
                            color = MaterialTheme.colorScheme.background,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        androidx.compose.material3.Button(
                            onClick = { 
                                forceBypassComplete = true
                                bypassStatus = "NORMAL"
                                if (isFailed) {
                                    isFailed = false
                                    isLoading = true
                                    retryTrigger++
                                }
                            },
                            modifier = Modifier
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                                .fillMaxWidth(),
                            colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                        ) {
                            Text(stringResource(R.string.verified_continue), color = MaterialTheme.colorScheme.onBackground)
                        }
                    }
                    
                    // The WebView block
                                                key(retryTrigger) {
                                AndroidView(
                                    modifier = Modifier.weight(1f).fillMaxWidth(),
                                    factory = { ctx ->
                                        WebView(ctx).apply {
                                            android.webkit.CookieManager.getInstance().setAcceptCookie(true)
                                            android.webkit.CookieManager.getInstance().setAcceptThirdPartyCookies(this, true)
                                            setInitialScale(1)
                                            settings.apply {
                                                javaScriptEnabled = true
                                                domStorageEnabled = true
                                                databaseEnabled = true
                                                javaScriptCanOpenWindowsAutomatically = true
                                                useWideViewPort = true
                                                loadWithOverviewMode = true
                                                setSupportZoom(true)
                                                builtInZoomControls = true
                                                displayZoomControls = false
                                                userAgentString = "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
                                                mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                                            }
                                            val cookieManager = android.webkit.CookieManager.getInstance()
                                            cookieManager.setAcceptCookie(true)
                                            cookieManager.setAcceptThirdPartyCookies(this, true)
                                            
                                            var lastFailedSiteIndex = -1
                                            val bridge = ServerSelectionBridge(
                                                onLogDebug = { msg ->
                                                    android.util.Log.d("AISTUDIO_DEBUG", msg)
                                                },
                                                onSendBypassStatus = { status ->
                                                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                        if (isFailed && bypassStatus != "CLOUDFLARE") return@post
                                                        if (status == "NORMAL" && (bypassStatus == "CHECKING_CLOUDFLARE" || bypassStatus == "CLOUDFLARE")) {
                                                            android.webkit.CookieManager.getInstance().flush()
                                                            bypassStatus = "VERIFIED"
                                                            android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                                                                if (bypassStatus == "VERIFIED") bypassStatus = "NORMAL"
                                                            }, 1500)
                                                        } else if (status == "CLOUDFLARE") {
                                                            val targetUrl = currentExtension.getSearchUrl("test", "test")
                                                            val cookies = android.webkit.CookieManager.getInstance().getCookie(targetUrl)
                                                            val hasCookies = cookies != null && cookies.isNotEmpty()
                                                            
                                                            if (!isFailed && !forceBypassComplete && !(hasCookies && !isManualBrowserOpen)) {
                                                                bypassStatus = "CLOUDFLARE"
                                                            }
                                                        }
                                                    }
                                                },
                                                onSendFailed = {
                                                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                        if (isManualBrowserOpen) return@post
                                                        if (bypassStatus == "CLOUDFLARE") return@post
                                                        if (lastFailedSiteIndex != currentSiteIndex) {
                                                            lastFailedSiteIndex = currentSiteIndex
                                                            currentSiteIndex++
                                                            retryTrigger++
                                                        }
                                                    }
                                                },
                                                onSendServersV2 = { serversJson, url ->
                                                    try {
                                                        android.util.Log.d("ExtServers", "sendServersV2 called with: " + serversJson)
                                                        val serversData = org.json.JSONArray(serversJson)
                                                        val serversNames = mutableListOf<String>()
                                                        val serversMap = mutableMapOf<String, String>()
                                                        val downloadsMap = mutableMapOf<String, String>()
                                                        val serversIds = mutableMapOf<String, String>()
                                                        
                                                        for (i in 0 until serversData.length()) {
                                                            val item = serversData.getJSONObject(i)
                                                            val name = item.getString("name")
                                                            val link = if (item.has("link")) item.getString("link") else if (item.has("url")) item.getString("url") else ""
                                                            val id = if (item.has("id")) item.getString("id") else ""
                                                            
                                                            if (name.contains("(تحميل)") || link.endsWith(".mp4") || link.endsWith(".mkv")) {
                                                                downloadsMap[name] = link
                                                            } else {
                                                                serversNames.add(name)
                                                                serversMap[name] = link
                                                                serversIds[name] = id
                                                            }
                                                        }
                                                        
                                                        if ((serversNames.isNotEmpty() || downloadsMap.isNotEmpty()) && extractedServers.isEmpty()) {
                                                            android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                                bypassStatus = "NORMAL"
                                                                finalWatchUrl = url
                                                                extractedServers = serversNames
                                                                extractedServerLinks = serversMap
                                                                extractedDownloadLinks = downloadsMap
                                                                extractedServerIds = serversIds
                                                                ServerStateStore.currentMediaKey = mediaKey
                                                                ServerStateStore.extractedServers = serversNames
                                                                ServerStateStore.extractedServerLinks = serversMap
                                                                ServerStateStore.extractedDownloadLinks = downloadsMap
                                                                extractedServerIds = serversIds
                                                                ServerStateStore.extractedServerIds = serversIds
                                                                isLoading = false
                                                            }
                                                        }
                                                    } catch (e: Exception) { e.printStackTrace() }
                                                },
                                                onSendServers = { serversStr, url ->
                                                    val servers = serversStr.split(",").filter { it.isNotBlank() }.distinct()
                                                    if (servers.isNotEmpty() && extractedServers.isEmpty()) {
                                                        android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                            bypassStatus = "NORMAL"
                                                            finalWatchUrl = url
                                                            extractedServers = servers
                                                            val tempMap = servers.associateWith { "" }
                                                            ServerStateStore.currentMediaKey = mediaKey
                                                            ServerStateStore.extractedServers = servers
                                                            ServerStateStore.extractedServerLinks = tempMap
                                                            extractedServerLinks = tempMap
                                                            isLoading = false
                                                        }
                                                    }
                                                }
                                            )
                                            addJavascriptInterface(bridge, "AndroidBridge")
                                            
                                            webChromeClient = object : android.webkit.WebChromeClient() {
                                                override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                    super.onProgressChanged(view, newProgress)
                                                    if (newProgress >= 30) {
                                                        val autoPlayScript = currentExtension.getExtractionScript(isMovie, episode, cleanTitleWithYear)
                                                        view?.evaluateJavascript(autoPlayScript, null)
                                                    }
                                                }
                                            }
                                            
                                            webViewClient = object : android.webkit.WebViewClient() {
                                                private var isNotified = false
                                                private var urlToCheck = ""
                                                private var checkAttempt = 0
                                                
                                                override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                                                    super.onPageStarted(view, url, favicon)
                                                    isNotified = false
                                                    checkAttempt = 0
                                                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                        // Removed: Do not auto-hide WebView on reload/navigate
                                                        // if (bypassStatus == "CLOUDFLARE") {
                                                        //     bypassStatus = "CHECKING_CLOUDFLARE"
                                                        // }
                                                    }
                                                }
                                                
                                                override fun onPageFinished(view: WebView?, url: String?) {
                                                    super.onPageFinished(view, url)
                                                    if (url != null) { urlToCheck = url }
                                                    if (!isNotified) { repeatCheck(view, 0) }
                                                }
                                                
                                                private fun repeatCheck(view: WebView?, attempt: Int) {
                                                    if (attempt > 30 || isNotified) return
                                                    
                                                    val checkJS = """
                                                        (function() {
                                                            var isCloudflare = document.getElementById('challenge-running') !== null ||
                                                                               document.querySelector('.cf-browser-verification') !== null ||
                                                                               document.querySelector('#cf-wrapper') !== null ||
                                                                               document.querySelector('#turnstile-wrapper') !== null ||
                                                                               document.body.innerHTML.indexOf('cf-turnstile') !== -1 ||
                                                                               document.title.toLowerCase().indexOf('just a moment') !== -1 ||
                                                                               document.title.toLowerCase().indexOf('attention required') !== -1 ||
                                                                               document.body.innerText.indexOf('Checking your browser') !== -1 ||
                                                                               document.body.innerText.indexOf('Verify you are human') !== -1;

                                                            if (isCloudflare) {
                                                                try { AndroidBridge.sendBypassStatus('CLOUDFLARE'); } catch (e) {}
                                                                return false;
                                                            }

                                                            var contentExists = document.querySelector('video') !== null ||
                                                                                document.querySelector('iframe') !== null ||
                                                                                document.querySelector('.download-btn') !== null ||
                                                                                document.getElementById('player-container') !== null ||
                                                                                document.body.innerText.length > 200;
                                                                                
                                                            return contentExists;
                                                        })();
                                                    """.trimIndent()

                                                    view?.evaluateJavascript(checkJS) { result ->
                                                        if (result == "true" && !isNotified) {
                                                            if (bypassStatus == "CLOUDFLARE" && !forceBypassComplete && !isManualBrowserOpen) {
                                                                android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                                                                    repeatCheck(view, attempt + 1)
                                                                }, 1000)
                                                                return@evaluateJavascript
                                                            }
                                                            
                                                            isNotified = true
                                                            android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                                android.webkit.CookieManager.getInstance().flush()
                                                                if (!isManualBrowserOpen && bypassStatus == "CHECKING_CLOUDFLARE") {
                                                                    bypassStatus = "NORMAL"
                                                                }
                                                                if (isFailed) {
                                                                    isFailed = false
                                                                    isLoading = true
                                                                }
                                                            }
                                                            val autoPlayScript = currentExtension.getExtractionScript(isMovie, episode, cleanTitleWithYear)
                                                            view?.evaluateJavascript(autoPlayScript, null)
                                                        } else {
                                                            android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                                                                repeatCheck(view, attempt + 1)
                                                            }, 1000)
                                                        }
                                                    }
                                                }
                                            }
                                            
                                            val targetUrl = searchUrl
                                            val cookies = android.webkit.CookieManager.getInstance().getCookie(targetUrl)
                                            if (!isManualBrowserOpen && cookies != null && cookies.isNotEmpty()) {
                                                bypassStatus = "NORMAL"
                                                forceBypassComplete = true
                                            }
                                            loadUrl(targetUrl)
                                        }
                                    }, onRelease = { it.stopLoading(); it.destroy() }
                                )
                            }
                }
            }
            

        if (!isCloudflare) {
            val displayTitle = when {
                isFailed || extractedServers.isNotEmpty() -> "اختر السيرفر"
                else -> "الاتصال بالسيرفر"
            }
            
            val displaySubtitle = when {
                isFailed -> "جاري الإتصال بالسيرفرات المتاحة..."
                isExtractingQuality -> "اختر جودة العرض المتاحة"
                extractedServers.isNotEmpty() -> "جاري جلب السيرفرات المتاحة..."
                isVerified || isNormal -> "تم الاتصال ..."
                else -> "جاري الاتصال..."
            }
            
            val displayIcon = when {
                isFailed -> androidx.compose.material.icons.Icons.Outlined.CloudOff
                extractedServers.isNotEmpty() && !isFailed -> if (isExtractingQuality) androidx.compose.material.icons.Icons.Outlined.Storage else androidx.compose.material.icons.Icons.Outlined.CloudDownload
                isVerified || isNormal -> androidx.compose.material.icons.Icons.Outlined.CloudDone
                else -> androidx.compose.material.icons.Icons.Outlined.CloudDownload
            }
            
            val iconTint = if (isFailed) Color(0xFFFF1111) else if (isVerified || isNormal) Color(0xFF00C853) else MaterialTheme.colorScheme.primary
            
            val isHorizontal = isLoading && !isCloudflare && extractedServers.isEmpty() && !isFailed
            
            Box(
                modifier = Modifier
                    .fillMaxWidth(0.95f)
                    .wrapContentHeight()
                    .clip(RoundedCornerShape(24.dp))
                    .background(Color(0xFF101014))
                    .border(1.dp, iconTint.copy(alpha = 0.3f), RoundedCornerShape(24.dp))
                    .clickable(
                        interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                        indication = null,
                        onClick = {}
                    )
            ) {
                Box(
                    modifier = Modifier
                        .matchParentSize()
                        .background(
                            androidx.compose.ui.graphics.Brush.radialGradient(
                                colors = listOf(iconTint.copy(alpha = 0.15f), Color.Transparent),
                                radius = 600f,
                                center = androidx.compose.ui.geometry.Offset(0f, 0f)
                            )
                        )
                )
                
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(20.dp)
                        .animateContentSize()
                ) {
                                        Box(
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Box(
                            modifier = Modifier
                                .align(Alignment.CenterStart)
                                .size(48.dp)
                                .background(iconTint.copy(alpha = 0.15f), CircleShape)
                                .border(1.dp, iconTint.copy(alpha = 0.3f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(displayIcon, contentDescription = null, tint = iconTint, modifier = Modifier.size(24.dp))
                        }
                        
                        Column(
                            modifier = Modifier.align(Alignment.Center).padding(horizontal = 56.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(displayTitle, color = Color.White, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, textAlign = androidx.compose.ui.text.style.TextAlign.Center, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(displaySubtitle, color = iconTint.copy(alpha = 0.8f), style = MaterialTheme.typography.bodySmall, textAlign = androidx.compose.ui.text.style.TextAlign.Center, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                            
                            if (isHorizontal) {
                                Spacer(modifier = Modifier.height(8.dp))
                                val progress = (currentSiteIndex.toFloat() / safeSites.size.coerceAtLeast(1).toFloat()).coerceIn(0f, 1f)
                                val animatedProgress by androidx.compose.animation.core.animateFloatAsState(targetValue = if (progress == 0f) 0.1f else progress)
                                Box(modifier = Modifier.fillMaxWidth(0.6f).height(4.dp).clip(CircleShape).background(Color(0xFF222222))) {
                                    Box(
                                        modifier = Modifier
                                            .fillMaxWidth(animatedProgress)
                                            .fillMaxHeight()
                                            .background(iconTint)
                                    )
                                }
                            }
                        }
                        
                        Box(
                            modifier = Modifier
                                .align(Alignment.CenterEnd)
                                .size(36.dp)
                                .background(Color(0xFF222225), CircleShape)
                                .border(1.dp, Color(0xFF333333), CircleShape)
                                .clip(CircleShape)
                                .clickable {
                                    if (isLoading || isExtractingQuality) {
                                        showCancelConfirmDialog = true
                                    } else {
                                        onDismiss()
                                    }
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Close, contentDescription = "إغلاق", tint = Color.White, modifier = Modifier.size(16.dp))
                        }
                    }
                    
                    if (!isHorizontal) {
                        Spacer(modifier = Modifier.height(24.dp))
                        
                        if (isFailed) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(Color(0xFF220000))
                                    .border(1.dp, Color(0x33FF1111), RoundedCornerShape(12.dp))
                                    .padding(16.dp)
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(androidx.compose.material.icons.Icons.Default.Error, contentDescription = null, tint = Color(0xFFFF1111), modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(12.dp))
                                    Text(
                                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                                        color = Color(0xFFFF4444),
                                        style = MaterialTheme.typography.bodySmall,
                                        lineHeight = 18.sp
                                    )
                                }
                            }
                            
                            Spacer(modifier = Modifier.height(24.dp))
                            
                            Button(
                                onClick = {
                                    isFailed = false
                                    isLoading = true
                                    currentSiteIndex = 0
                                    currentExtension = safeSites[0]
                                    retryTrigger++
                                },
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFF1111)),
                                shape = RoundedCornerShape(24.dp)
                            ) {
                                Icon(androidx.compose.material.icons.Icons.Default.Refresh, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(stringResource(R.string.retry_again), color = Color.White, fontWeight = FontWeight.Bold)
                            }
                            
                            Spacer(modifier = Modifier.height(12.dp))
                            
                            Button(
                                onClick = { showOpenBrowserConfirmDialog = true },
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF222225)),
                                shape = RoundedCornerShape(24.dp)
                            ) {
                                Icon(androidx.compose.material.icons.Icons.Default.OpenInBrowser, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(stringResource(R.string.open_browser_manual), color = Color.LightGray, fontWeight = FontWeight.Medium)
                            }
                            
                            Spacer(modifier = Modifier.height(12.dp))
                            
                            Button(
                                onClick = { showSkipSiteConfirmDialog = true },
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF222225)),
                                shape = RoundedCornerShape(24.dp)
                            ) {
                                Icon(androidx.compose.material.icons.Icons.Default.Language, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(stringResource(R.string.skip_current), color = Color.LightGray, fontWeight = FontWeight.Medium)
                            }
                            
                            if (showOpenBrowserConfirmDialog) {
                                androidx.compose.material3.AlertDialog(
                                    onDismissRequest = { showOpenBrowserConfirmDialog = false },
                                    title = { Text(stringResource(R.string.confirm_browser), color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text(stringResource(R.string.confirm_open_browser), color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                isManualBrowserOpen = true
                                                forceBypassComplete = false
                                                showOpenBrowserConfirmDialog = false
                                                isFailed = false
                                                isLoading = true
                                                currentSiteIndex = 0
                                                currentExtension = safeSites[0]
                                                android.webkit.CookieManager.getInstance().removeAllCookies(null)
                                                android.webkit.CookieManager.getInstance().flush()
                                                bypassStatus = "CLOUDFLARE"
                                                retryTrigger++
                                            }
                                        ) { Text(stringResource(R.string.yes_ar), color = MaterialTheme.colorScheme.primary) }
                                    },
                                    dismissButton = {
                                        androidx.compose.material3.TextButton(onClick = { showOpenBrowserConfirmDialog = false }) { Text(stringResource(R.string.cancel_ar), color = MaterialTheme.colorScheme.onBackground) }
                                    }
                                )
                            }
                            if (showSkipSiteConfirmDialog) {
                                androidx.compose.material3.AlertDialog(
                                    onDismissRequest = { showSkipSiteConfirmDialog = false },
                                    title = { Text(stringResource(R.string.confirm_skip), color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text(stringResource(R.string.confirm_skip_site), color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                showSkipSiteConfirmDialog = false
                                                if (currentSiteIndex < safeSites.size - 1) {
                                                    isFailed = false
                                                    isLoading = true
                                                    currentSiteIndex++
                                                    currentExtension = safeSites[currentSiteIndex]
                                                    bypassStatus = "CLOUDFLARE"
                                                    isManualBrowserOpen = false
                                                    forceBypassComplete = false
                                                    retryTrigger++
                                                } else {
                                                    showNoMoreExtensionsDialog = true
                                                }
                                            }
                                        ) { Text(stringResource(R.string.yes_ar), color = MaterialTheme.colorScheme.primary) }
                                    },
                                    dismissButton = {
                                        androidx.compose.material3.TextButton(onClick = { showSkipSiteConfirmDialog = false }) { Text(stringResource(R.string.cancel_ar), color = MaterialTheme.colorScheme.onBackground) }
                                    }
                                )
                            }
                            if (showNoMoreExtensionsDialog) {
                                AlertDialog(
                                    onDismissRequest = { showNoMoreExtensionsDialog = false },
                                    title = { Text("لا يوجد مواقع أخرى", color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text("عذراً، فشل البحث في جميع المواقع المتاحة.", color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        TextButton(
                                            onClick = {
                                                showNoMoreExtensionsDialog = false
                                                onDismiss()
                                            }
                                        ) {
                                            Text("إغلاق", color = MaterialTheme.colorScheme.primary)
                                        }
                                    }
                                )
                            }
                        } else if (selectedServerForQuality == null) {
                            LazyColumn(
                                modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                items(extractedServers) { server ->
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clip(RoundedCornerShape(16.dp))
                                            .background(Color(0xFF16161A))
                                            .border(1.dp, Color(0xFF222225), RoundedCornerShape(16.dp))
                                            .clickable {
                                                val finalUrl = extractedServerLinks[server] ?: ""
                                                val dLink = extractedDownloadLinks[server] ?: ""
                                                val watchUrl = if (finalUrl.contains("akamaized.net") || finalUrl.endsWith(".m3u8") || finalUrl.endsWith(".mp4")) {
                                                    finalUrl
                                                } else if (dLink.isNotEmpty()) {
                                                    dLink
                                                } else {
                                                    finalUrl
                                                }
                                                if (isDownloadMode) {
                                                    if (watchUrl.contains(".mp4")) {
                                                        com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList()
                                                        onPlay(watchUrl, server, currentSiteName)
                                                    } else {
                                                        selectedServerForQuality = server
                                                        isExtractingQuality = true
                                                        qualityExtractionMessage = "جاري استخراج الجودات لـ $server..."
                                                        if (watchUrl.contains(".m3u8") || watchUrl.contains("akamaized.net")) {
                                                            coroutineScope.launch {
                                                                val q = com.example.utils.M3U8Parser.getQualities(watchUrl)
                                                                extractedQualities = q
                                                                com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                                                isExtractingQuality = false
                                                            }
                                                        } else {
                                                            extractingEmbedUrl = watchUrl
                                                        }
                                                    }
                                                } else {
                                                    com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList() // clear so we fetch fresh
                                                    onPlay(watchUrl, server, currentSiteName)
                                                }
                                            }
                                            .padding(12.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Box(
                                            modifier = Modifier.size(32.dp).background(MaterialTheme.colorScheme.primary.copy(alpha=0.15f), CircleShape),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Icon(Icons.Filled.PlayArrow, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                                        }
                                        Spacer(modifier = Modifier.width(16.dp))
                                        Text(server, color = Color.White, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                                        Spacer(modifier = Modifier.weight(1f))
                                        Icon(androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
                                    }
                                }
                            }
                        } else {
                            if (isExtractingQuality) {
                                Box(modifier = Modifier.fillMaxWidth().height(150.dp), contentAlignment = Alignment.Center) {
                                    CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                                }
                            } else {
                                LazyColumn(
                                    modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp),
                                    verticalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    items(extractedQualities) { quality ->
                                        Row(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .clip(RoundedCornerShape(16.dp))
                                                .background(Color(0xFF16161A))
                                                .border(1.dp, Color(0xFF222225), RoundedCornerShape(16.dp))
                                                .clickable {
                                                    onPlay(quality.url, selectedServerForQuality ?: "", currentSiteName)
                                                }
                                                .padding(12.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Box(
                                                modifier = Modifier.size(32.dp).background(Color(0x15FFFFFF), CircleShape),
                                                contentAlignment = Alignment.Center
                                            ) {
                                                Icon(Icons.Filled.PlayArrow, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                                            }
                                            Spacer(modifier = Modifier.width(16.dp))
                                            Text(quality.name, color = Color.White, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                                            Spacer(modifier = Modifier.weight(1f))
                                            
                                            val badgeColor = when {
                                                quality.name.contains("1080") || quality.name.contains("FHD") -> Color(0xFFE91E63)
                                                quality.name.contains("720") || quality.name.contains("HD") -> Color(0xFF9C27B0)
                                                else -> Color(0xFF607D8B)
                                            }
                                            val badgeText = when {
                                                quality.name.contains("1080") || quality.name.contains("FHD") -> "FHD"
                                                quality.name.contains("720") || quality.name.contains("HD") -> "HD"
                                                else -> "SD"
                                            }
                                            Box(
                                                modifier = Modifier.background(badgeColor.copy(alpha=0.2f), RoundedCornerShape(8.dp)).padding(horizontal = 8.dp, vertical = 4.dp)
                                            ) {
                                                Text(badgeText, color = badgeColor, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                            }
                                        }
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = "يمكنك التبديل إلى سيرفر آخر لاحقاً",
                                    color = Color.Gray,
                                    fontSize = 12.sp,
                                    textAlign = TextAlign.Center,
                                    modifier = Modifier.fillMaxWidth()
                                )
                            }
                        }
                    }
                }
            }
        }

}
}

        extractingEmbedUrl?.let { url ->
            Box(modifier = Modifier.size(1.dp).alpha(0f)) {
                com.example.ui.screens.player.HiddenVideoExtractor(
                    url = url,
                    isMovie = isMovie,
                    season = season,
                    episode = episode,
                    targetServer = selectedServerForQuality,
                    targetServerId = if (selectedServerForQuality != null) extractedServerIds[selectedServerForQuality] else null,
                    website = currentSiteName,
                    title = title,
                    onVideoUrlFound = { extractedUrl ->
                        coroutineScope.launch {
                            val q = com.example.utils.M3U8Parser.getQualities(extractedUrl)
                            if (q.isNotEmpty()) {
                                extractedQualities = q
                                com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                isExtractingQuality = false
                            } else {
                                // Direct MP4 or unknown
                                extractedQualities = listOf(com.example.utils.M3U8Parser.QualityInfo("Default", extractedUrl))
                                com.example.ui.screens.player.ServerStateStore.extractedQualities = extractedQualities
                                isExtractingQuality = false
                            }
                            extractingEmbedUrl = null
                        }
                    },
                    onIframeUrlFound = { iframeUrl ->
                        extractingEmbedUrl = iframeUrl
                    },
                    onExtractionFailed = {
                        isExtractingQuality = false
                        extractingEmbedUrl = null
                        qualityExtractionMessage = "فشل استخراج الجودات"
                    }
                )
            }
        }
}
@Composable
fun StatusBadge(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, statusColor: Color, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .clip(RoundedCornerShape(14.dp))
            .background(MaterialTheme.colorScheme.surface)
            .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(14.dp))
            .padding(horizontal = 4.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(12.dp))
        Spacer(modifier = Modifier.width(2.dp))
        Text(text, color = Color.LightGray, fontSize = 9.sp, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
        Spacer(modifier = Modifier.width(2.dp))
        Box(modifier = Modifier.size(6.dp).background(statusColor, CircleShape))
}}

class ServerSelectionBridge(
    private val onLogDebug: (String) -> Unit,
    private val onSendBypassStatus: (String) -> Unit,
    private val onSendFailed: () -> Unit,
    private val onSendServersV2: (String, String) -> Unit,
    private val onSendServers: (String, String) -> Unit
) {
    @android.webkit.JavascriptInterface
    fun logDebug(msg: String) { onLogDebug(msg) }

    @android.webkit.JavascriptInterface
    fun sendBypassStatus(status: String) { onSendBypassStatus(status) }

    @android.webkit.JavascriptInterface
    fun sendFailed() { onSendFailed() }

    @android.webkit.JavascriptInterface
    fun sendServersV2(serversJson: String, url: String) { onSendServersV2(serversJson, url) }

    @android.webkit.JavascriptInterface
    fun sendServers(serversStr: String, url: String) { onSendServers(serversStr, url) }
}