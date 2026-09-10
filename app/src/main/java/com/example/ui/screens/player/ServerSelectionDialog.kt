package com.example.ui.screens.player

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
    isMovie: Boolean,
    season: Int = 1,
    episode: Int = 1,
    isAnime: Boolean = false,
    onDismiss: () -> Unit,
    onPlay: (url: String, serverName: String, website: String) -> Unit,
    onNavigateToExtensions: () -> Unit = {}
) {
    val coroutineScope = rememberCoroutineScope()
    
    
    val installedExtensions = ExtensionManager.installedExtensions.collectAsState().value
    val prioritySites = installedExtensions.filter { 
        if (isAnime) it.isAnime else if (isMovie) it.isMovie else it.isSeries 
    }
    val safeSites = if (prioritySites.isNotEmpty()) prioritySites else installedExtensions
    
    var currentSiteIndex by remember { mutableStateOf(0) }
    var currentExtension by remember { mutableStateOf(safeSites[0]) }
    val currentSiteName = currentExtension.name
    
    var isLoading by remember { mutableStateOf(true) }
    var loadingMessage by remember { mutableStateOf("جاري الفحص وتخطي الحماية...") }
    
    var extractedServers by remember { mutableStateOf<List<String>>(emptyList()) }
    var extractedServerLinks by remember { mutableStateOf<Map<String, String>>(emptyMap()) }
    var finalWatchUrl by remember { mutableStateOf<String?>(null) }
    var isFailed by remember { mutableStateOf(false) }
    var bypassStatus by remember { mutableStateOf("CHECKING_CLOUDFLARE") }
    var showCancelConfirmDialog by remember { mutableStateOf(false) }
    var isNetworkError by remember { mutableStateOf(false) }
    var retryTrigger by remember { mutableIntStateOf(0) }
    var showManualConfirmDialog by remember { mutableStateOf(false) }
    var showOpenBrowserConfirmDialog by remember { mutableStateOf(false) }
    var showSkipSiteConfirmDialog by remember { mutableStateOf(false) }
    var showNoMoreExtensionsDialog by remember { mutableStateOf(false) }

    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }


    // --- Quality Extraction States ---
    var selectedServerForQuality by remember { mutableStateOf<String?>(null) }
    var isExtractingQuality by remember { mutableStateOf(false) }
    var qualityExtractionMessage by remember { mutableStateOf("جاري استخراج الجودات المتاحة...") }
    var extractedQualities by remember { mutableStateOf<List<com.example.utils.M3U8Parser.QualityInfo>>(emptyList()) }

    LaunchedEffect(currentSiteIndex) {
        if (currentSiteIndex >= prioritySites.size) {
            isLoading = false
            isFailed = true
            return@LaunchedEffect
        }
        
        currentExtension = safeSites[currentSiteIndex]
        bypassStatus = "CHECKING_CLOUDFLARE"
        loadingMessage = "جاري الفحص في موقع $currentSiteName..."
        extractedServers = emptyList()
        finalWatchUrl = null
        
        // Wait for up to 30 iterations, but pause counting if we are doing Cloudflare bypass
        var waited = 0
        while (waited < 30) {
            delay(1000)
            if (bypassStatus != "CLOUDFLARE" && bypassStatus != "CHECKING_CLOUDFLARE") {
                waited++
            }
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
    val cleanTitle = baseTitle.replace(Regex("[^a-zA-Z0-9\\s]"), " ").replace(Regex("\\s+"), " ").trim()
    // For sites like tv10.egydead.live we actually need the original encoded title, not the cleaned one!
    // Example: tv10.egydead.live/?s=Spider-Man%3A+Brand+New+Day
    val encodedTitleOriginal = URLEncoder.encode(baseTitle, "UTF-8")
    val encodedPlusTitleOriginal = URLEncoder.encode(baseTitle, "UTF-8").replace("%20", "+")
    val encodedTitle = URLEncoder.encode(cleanTitle, "UTF-8")
    val encodedPlusTitle = URLEncoder.encode(cleanTitle, "UTF-8").replace("%20", "+")
    
    // We use the original encoded title for all sites as requested, so we don't break their search
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
                        .background(Color.White)
                        .zIndex(100f)
                } else {
                    Modifier.size(1.dp).alpha(0.01f).zIndex(-1f)
                }
            ) {
                Column(modifier = Modifier.fillMaxSize()) {
                    if (isCloudflare) {
                        Text(
                            text = "يرجى تخطي الحماية للمتابعة...",
                            modifier = Modifier
                                .padding(16.dp)
                                .fillMaxWidth(),
                            textAlign = TextAlign.Center,
                            color = Color.Black,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        androidx.compose.material3.Button(
                            onClick = { showManualConfirmDialog = true },
                            modifier = Modifier
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                                .fillMaxWidth(),
                            colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                        ) {
                            Text("تم التحقق، متابعة", color = Color.White)
                        }
                    }
                    
                    // The WebView block
                                                key(retryTrigger) {
                                AndroidView(
                                    modifier = Modifier.fillMaxSize(),
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
                                            
                                            addJavascriptInterface(object {
                                                private var lastFailedSiteIndex = -1
                                                @android.webkit.JavascriptInterface
                                                fun logDebug(msg: String) {
                                                    android.util.Log.d("AISTUDIO_DEBUG", msg)
                                                }
                                                @android.webkit.JavascriptInterface
                                                fun sendBypassStatus(status: String) {
                                                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                        if (status == "NORMAL" && (bypassStatus == "CHECKING_CLOUDFLARE" || bypassStatus == "CLOUDFLARE")) {
                                                            android.webkit.CookieManager.getInstance().flush()
                                                            bypassStatus = "VERIFIED"
                                                            android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                                                                if (bypassStatus == "VERIFIED") bypassStatus = "NORMAL"
                                                            }, 1500)
                                                        } else if (status == "CLOUDFLARE") {
                                                            bypassStatus = "CLOUDFLARE"
                                                        }
                                                    }
                                                }
                                                @android.webkit.JavascriptInterface
                                                fun sendFailed() {
                                                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                        if (lastFailedSiteIndex != currentSiteIndex) {
                                                            lastFailedSiteIndex = currentSiteIndex
                                                            currentSiteIndex++
                                                        }
                                                    }
                                                }
                                                @android.webkit.JavascriptInterface
                                                fun sendServersV2(serversJson: String, url: String) {
                                                    try {
                                                        val serversData = org.json.JSONArray(serversJson)
                                                        val serversNames = mutableListOf<String>()
                                                        val serversMap = mutableMapOf<String, String>()
                                                        val serversIds = mutableMapOf<String, String>()
                                                        
                                                        for (i in 0 until serversData.length()) {
                                                            val item = serversData.getJSONObject(i)
                                                            val name = item.getString("name")
                                                            val link = if (item.has("link")) item.getString("link") else if (item.has("url")) item.getString("url") else ""
                                                            val id = if (item.has("id")) item.getString("id") else ""
                                                            serversNames.add(name)
                                                            serversMap[name] = link
                                                            serversIds[name] = id
                                                        }
                                                        
                                                        if (serversNames.isNotEmpty() && extractedServers.isEmpty()) {
                                                            android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                                finalWatchUrl = url
                                                                extractedServers = serversNames
                                                                extractedServerLinks = serversMap
                                                                com.example.ui.screens.player.ServerStateStore.extractedServers = serversNames
                                                                com.example.ui.screens.player.ServerStateStore.extractedServerLinks = serversMap
                                                                com.example.ui.screens.player.ServerStateStore.extractedServerIds = serversIds
                                                                isLoading = false
                                                            }
                                                        }
                                                    } catch (e: Exception) { e.printStackTrace() }
                                                }
                                                @android.webkit.JavascriptInterface
                                                fun sendServers(serversStr: String, url: String) {
                                                    val servers = serversStr.split(",").filter { it.isNotBlank() }.distinct()
                                                    if (servers.isNotEmpty() && extractedServers.isEmpty()) {
                                                        android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                            finalWatchUrl = url
                                                            extractedServers = servers
                                                            val tempMap = servers.associateWith { "" }
                                                            com.example.ui.screens.player.ServerStateStore.extractedServers = servers
                                                            com.example.ui.screens.player.ServerStateStore.extractedServerLinks = tempMap
                                                            extractedServerLinks = tempMap
                                                            isLoading = false
                                                        }
                                                    }
                                                }
                                            }, "AndroidBridge")
                                            
                                            webChromeClient = object : android.webkit.WebChromeClient() {
                                                override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                    super.onProgressChanged(view, newProgress)
                                                    if (newProgress >= 30) {
                                                        val autoPlayScript = currentExtension.getExtractionScript(isMovie, episode, title)
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
                                                        if (bypassStatus == "CLOUDFLARE") {
                                                            bypassStatus = "CHECKING_CLOUDFLARE"
                                                        }
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
                                                            isNotified = true
                                                            android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                                android.webkit.CookieManager.getInstance().flush()
                                                                bypassStatus = "NORMAL"
                                                            }
                                                            val autoPlayScript = currentExtension.getExtractionScript(isMovie, episode, title)
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
                                            loadUrl(targetUrl)
                                        }
                                    }
                                )
                            }
                }
            }
            
            if (!isCloudflare) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(0.95f)

                .wrapContentHeight()
                .clip(RoundedCornerShape(24.dp))
                .background(Color(0xFF16161A))
                .border(1.dp, Color(0x33FF1111), RoundedCornerShape(24.dp))
                .clickable(
                    interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                    indication = null,
                    onClick = {} // Consume clicks inside the dialog so they don't dismiss
                )
        ) {
            // Subtle top-left / top-right radial gradient for the red glow
            Box(
                modifier = Modifier
                    .matchParentSize()
                    .background(
                        Brush.radialGradient(
                            colors = listOf(Color(0x15FF1111), Color.Transparent),
                            radius = 600f,
                            center = androidx.compose.ui.geometry.Offset(0f, 0f)
                        )
                    )
            )

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(Color(0xFF330000), CircleShape)
                            .clickable {
                                if (selectedServerForQuality != null) {
                                    selectedServerForQuality = null
                                    extractedQualities = emptyList()
                                    isExtractingQuality = false
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = if (selectedServerForQuality != null) androidx.compose.material.icons.Icons.Default.ArrowBack else androidx.compose.material.icons.Icons.Outlined.CloudDownload,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(24.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(
                        modifier = Modifier.weight(1f),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "اختر السيرفر",
                            color = Color.White,
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                        )
                        Text(
                            text = "جاري الإتصال بالسيرفرات المتاحة...",
                            color = Color.Gray,
                            style = MaterialTheme.typography.bodySmall,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                        )
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    IconButton(
                        onClick = {
                            if (isLoading) {
                                showCancelConfirmDialog = true
                            } else {
                                onDismiss()
                            }
                        },
                        modifier = Modifier
                            .size(36.dp)
                            .background(Color(0xFF222225), CircleShape)
                            .border(1.dp, Color(0xFF333333), CircleShape)
                    ) {
                        Icon(Icons.Default.Close, contentDescription = "إغلاق", tint = Color.White, modifier = Modifier.size(18.dp))
                    }
                }

                Spacer(modifier = Modifier.height(32.dp))



                if (isLoading && !isFailed) {
                    androidx.compose.animation.AnimatedContent(
                        targetState = bypassStatus,
                        transitionSpec = {
                            androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) togetherWith androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300))
                        }, label = "BypassAnimation"
                    ) { currentStatus ->
                        Box(
                            modifier = Modifier.fillMaxWidth().height(450.dp).clip(androidx.compose.foundation.shape.RoundedCornerShape(12.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            // 1. The WebView (Always present, but hidden by overlay if not Cloudflare)
/* WEBVIEW WAS HERE */
                            
                            

                            // 2. The Overlay UI (Shown when NOT CLOUDFLARE)
                            if (currentStatus != "CLOUDFLARE") {
                                Box(
                                    modifier = Modifier.fillMaxSize().background(Color(0xFF16161A)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    if (isNetworkError) {
                                        Column(
                                            horizontalAlignment = Alignment.CenterHorizontally,
                                            modifier = Modifier.padding(16.dp)
                                        ) {
                                            Icon(
                                                imageVector = androidx.compose.material.icons.Icons.Default.Close,
                                                contentDescription = "Network Error",
                                                tint = Color(0xFFFF1111),
                                                modifier = Modifier.size(64.dp)
                                            )
                                            Spacer(modifier = Modifier.height(16.dp))
                                            Text(
                                                text = "حدث خطأ في الاتصال بالإنترنت",
                                                color = Color.White,
                                                style = MaterialTheme.typography.titleMedium,
                                                fontWeight = FontWeight.Bold
                                            )
                                            Spacer(modifier = Modifier.height(8.dp))
                                            Text(
                                                text = "يرجى التحقق من الشبكة والمحاولة مرة أخرى.",
                                                color = Color.Gray,
                                                style = MaterialTheme.typography.bodySmall
                                            )
                                            Spacer(modifier = Modifier.height(24.dp))
                                            Button(
                                                onClick = { 
                                                    isNetworkError = false
                                                    retryTrigger++ 
                                                },
                                                colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = activeColor),
                                                shape = RoundedCornerShape(12.dp)
                                            ) {
                                                Text("إعادة المحاولة", color = Color.White, fontWeight = FontWeight.Bold)
                                            }
                                        }
                                    } else {
                                        Column(
                                            horizontalAlignment = Alignment.CenterHorizontally,
                                            modifier = Modifier.padding(16.dp)
                                        ) {
                                            Box(
                                                contentAlignment = Alignment.Center,
                                                modifier = Modifier.size(140.dp)
                                            ) {
                                                androidx.compose.foundation.Canvas(modifier = Modifier.size(140.dp)) {
                                                    drawCircle(
                                                        color = Color(0x15FF1111),
                                                        radius = size.minDimension / 2,
                                                        style = androidx.compose.ui.graphics.drawscope.Stroke(width = 1.dp.toPx())
                                                    )
                                                    drawCircle(
                                                        color = Color(0x25FF1111),
                                                        radius = size.minDimension / 2 - 20f,
                                                        style = androidx.compose.ui.graphics.drawscope.Stroke(width = 1.dp.toPx())
                                                    )
                                                }
                                                CircularProgressIndicator(
                                                    color = activeColor,
                                                    trackColor = Color(0xFF222225),
                                                    modifier = Modifier.size(90.dp),
                                                    strokeWidth = 6.dp
                                                )
                                            }
                                            Spacer(modifier = Modifier.height(32.dp))
                                            val statusMsg = when (bypassStatus) {
                                                "CHECKING_CLOUDFLARE" -> {
                                                    androidx.compose.ui.text.buildAnnotatedString {
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تأمين الاتصال بموقع ") }
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                                                    }
                                                }
                                                "CLOUDFLARE" -> {
                                                    androidx.compose.ui.text.buildAnnotatedString {
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تخطي حماية ") }
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFFFF1111))) { append("Cloudflare") }
                                                    }
                                                }
                                                "VERIFIED" -> {
                                                    androidx.compose.ui.text.buildAnnotatedString {
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تم التخطي ") }
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append("بنجاح") }
                                                    }
                                                }
                                                else -> {
                                                    androidx.compose.ui.text.buildAnnotatedString {
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري البحث في ") }
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                                                    }
                                                }
                                            }
                                            Text(
                                                text = statusMsg,
                                                style = MaterialTheme.typography.titleMedium,
                                                fontWeight = FontWeight.Bold,
                                                textAlign = TextAlign.Center,
                                                maxLines = 1,
                                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                                                modifier = Modifier.fillMaxWidth()
                                            )
                                            Spacer(modifier = Modifier.height(8.dp))
                                            Text(
                                                text = "الرجاء الإنتظار، يتم جلب أحدث المعلومات من السيرفرات.",
                                                color = Color.Gray,
                                                style = MaterialTheme.typography.bodySmall,
                                                textAlign = TextAlign.Center,
                                                maxLines = 1,
                                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                                                modifier = Modifier.fillMaxWidth()
                                            )
                                            Spacer(modifier = Modifier.height(32.dp))
                                            Row(
                                                modifier = Modifier.fillMaxWidth(),
                                                horizontalArrangement = Arrangement.spacedBy(4.dp, Alignment.CenterHorizontally),
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                StatusBadge(
                                                    text = "جاري التحقق",
                                                    icon = androidx.compose.material.icons.Icons.Outlined.Storage,
                                                    statusColor = activeColor
                                                )
                                                StatusBadge(
                                                    text = "جلب السيرفرات",
                                                    icon = androidx.compose.material.icons.Icons.Outlined.Sync,
                                                    statusColor = activeColor
                                                )
                                                StatusBadge(
                                                    text = "اتصال آمن",
                                                    icon = androidx.compose.material.icons.Icons.Outlined.Security,
                                                    statusColor = if (bypassStatus == "VERIFIED" || bypassStatus == "NORMAL") Color(0xFF00C853) else Color.Gray
                                                )
                                            }
                                            Spacer(modifier = Modifier.height(24.dp))
                                        }
                                    }
                                }
                            }
                        }
                    } // End AnimatedContent
                    
                    
                    // Bottom progress line
                    val progress = (currentSiteIndex.toFloat() / prioritySites.size.coerceAtLeast(1).toFloat()).coerceIn(0f, 1f)
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(4.dp)
                            .clip(RoundedCornerShape(2.dp))
                            .background(Color(0xFF222225))
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth(if (progress == 0f) 0.1f else progress)
                                .height(4.dp)
                                .background(activeColor)
                        )
                    }
                } else if (isFailed) {
                    Text(
                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                        color = Color(0xFFFF1111),
                        style = MaterialTheme.typography.bodyLarge,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(24.dp))
                    Button(
                        onClick = {
                            isFailed = false
                            isLoading = true
                            currentSiteIndex = 0
                            currentExtension = safeSites[0]
                            retryTrigger++
                        },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                    ) {
                        Text("إعادة المحاولة مجدداً", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Button(
                        onClick = {
                            showOpenBrowserConfirmDialog = true
                        },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color.DarkGray)
                    ) {
                        Text("فتح المتصفح يدوياً للتحقق", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Button(
                        onClick = {
                            showSkipSiteConfirmDialog = true
                        },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color.DarkGray)
                    ) {
                        Text("تخطي الموقع الحالي", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                    
                    if (showOpenBrowserConfirmDialog) {
                        androidx.compose.material3.AlertDialog(
                            onDismissRequest = { showOpenBrowserConfirmDialog = false },
                            title = { Text("تأكيد فتح المتصفح", color = Color.White) },
                            text = { Text("هل أنت متأكد من رغبتك في فتح المتصفح يدوياً للتحقق من الرابط؟", color = Color.LightGray) },
                            containerColor = Color(0xFF222225),
                            confirmButton = {
                                androidx.compose.material3.TextButton(
                                    onClick = {
                                        showOpenBrowserConfirmDialog = false
                                        bypassStatus = "CLOUDFLARE"
                                    }
                                ) { Text("نعم", color = Color(0xFFE50914)) }
                            },
                            dismissButton = {
                                androidx.compose.material3.TextButton(onClick = { showOpenBrowserConfirmDialog = false }) { Text("إلغاء", color = Color.White) }
                            }
                        )
                    }
                    
                    if (showSkipSiteConfirmDialog) {
                        androidx.compose.material3.AlertDialog(
                            onDismissRequest = { showSkipSiteConfirmDialog = false },
                            title = { Text("تأكيد التخطي", color = Color.White) },
                            text = { Text("هل أنت متأكد من رغبتك في تخطي هذا الموقع والانتقال للتالي؟", color = Color.LightGray) },
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
                                            bypassStatus = "CHECKING_CLOUDFLARE"
                                            retryTrigger++
                                        } else {
                                            showNoMoreExtensionsDialog = true
                                        }
                                    }
                                ) { Text("نعم", color = Color(0xFFE50914)) }
                            },
                            dismissButton = {
                                androidx.compose.material3.TextButton(onClick = { showSkipSiteConfirmDialog = false }) { Text("إلغاء", color = Color.White) }
                            }
                        )
                    }
                    if (showNoMoreExtensionsDialog) {
                        androidx.compose.material3.AlertDialog(
                            onDismissRequest = { showNoMoreExtensionsDialog = false },
                            title = { Text("لا توجد إضافات أخرى", color = Color.White) },
                            text = { Text("لم يتم تثبيت أي إضافات أخرى للمتابعة. ماذا تريد أن تفعل؟", color = Color.LightGray) },
                            containerColor = Color(0xFF222225),
                            confirmButton = {
                                Row {
                                    androidx.compose.material3.TextButton(
                                        onClick = {
                                            showNoMoreExtensionsDialog = false
                                        }
                                    ) { Text("العودة", color = Color(0xFF00C853)) }
                                    androidx.compose.material3.TextButton(
                                        onClick = {
                                            showNoMoreExtensionsDialog = false
                                            showCancelConfirmDialog = true
                                        }
                                    ) { Text("إلغاء تماماً", color = Color(0xFFE50914)) }
                                }
                            },
                            dismissButton = {
                                androidx.compose.material3.TextButton(onClick = { 
                                    showNoMoreExtensionsDialog = false
                                    onDismiss()
                                }) { Text("إغلاق وإضافة مواقع", color = Color.White) }
                            }
                        )
                    }
                } else if (extractedServers.isNotEmpty()) {
                    if (selectedServerForQuality != null) {
                        if (isExtractingQuality) {
                            CircularProgressIndicator(
                                color = Color(0xFFE50914),
                                modifier = Modifier.size(50.dp)
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Text(
                                text = qualityExtractionMessage,
                                color = Color.White,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                textAlign = TextAlign.Center,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "السيرفر: $selectedServerForQuality",
                                color = Color.Gray,
                                style = MaterialTheme.typography.bodySmall
                            )
                        } else if (extractedQualities.isNotEmpty()) {
                            Text(
                                text = "اختر الجودة ($selectedServerForQuality)",
                                color = Color(0xFFE50914),
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                            
                            LazyColumn(
                                modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                items(extractedQualities) { quality ->
                                    Card(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clickable {
                                                val serverNameOnly = selectedServerForQuality ?: "سيرفر"
                                                onPlay(quality.url, serverNameOnly, currentSiteName)
                                            },
                                        colors = CardDefaults.cardColors(
                                            containerColor = Color(0xFF222225)
                                        ),
                                        shape = RoundedCornerShape(12.dp)
                                    ) {
                                        Row(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .padding(16.dp),
                                            verticalAlignment = Alignment.CenterVertically,
                                            horizontalArrangement = Arrangement.Center
                                        ) {
                                            Text(
                                                text = quality.name,
                                                color = Color.White,
                                                style = MaterialTheme.typography.titleMedium,
                                                fontWeight = FontWeight.Bold
                                            )
                                        }
                                    }
                                }
                            }
                            
                            Spacer(modifier = Modifier.height(16.dp))
                            TextButton(onClick = { 
                                selectedServerForQuality = null
                                extractedQualities = emptyList()
                            }) {
                                Text("العودة لاختيار سيرفر آخر", color = Color.LightGray)
                            }
                        }
                    } else {
                        Text(
                            text = "تم جلب السيرفرات من: $currentSiteName",
                            color = Color(0xFF00C853),
                            style = MaterialTheme.typography.labelLarge,
                            modifier = Modifier.padding(bottom = 16.dp)
                        )
                        
                        LazyColumn(
                            modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            items(extractedServers) { server ->
                                Card(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable {
                                            selectedServerForQuality = server
                                            isExtractingQuality = true
                                            extractedQualities = emptyList()
                                        },
                                    colors = CardDefaults.cardColors(
                                        containerColor = Color(0xFF222225)
                                    ),
                                    shape = RoundedCornerShape(12.dp)
                                ) {
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .padding(16.dp),
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.Center
                                    ) {
                                        Text(
                                            text = server,
                                            color = Color.White,
                                            style = MaterialTheme.typography.titleMedium,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                }
                            }
                        }
                        
                        if (currentSiteIndex < prioritySites.size - 1) {
                            Spacer(modifier = Modifier.height(16.dp))
                            TextButton(
                                onClick = {
                                    currentSiteIndex++
                                    currentExtension = safeSites[currentSiteIndex]
                                    extractedServers = emptyList()
                                    extractedServerLinks = emptyMap()
                                    isLoading = true
                                    isFailed = false
                                    bypassStatus = "CHECKING_CLOUDFLARE"
                                    retryTrigger++
                                },
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Text("البحث في موقع آخر", color = Color(0xFF00C853))
                            }
                        }
                    }
                }
        
            }

                if (showManualConfirmDialog) {
                    androidx.compose.material3.AlertDialog(
                        onDismissRequest = { showManualConfirmDialog = false },
                        title = { Text("تأكيد", color = Color.White) },
                        text = { Text("هل أنت متأكد أنك قمت بتخطي حماية Cloudflare بنجاح؟", color = Color.LightGray) },
                        containerColor = Color(0xFF222225),
                        confirmButton = {
                            androidx.compose.material3.TextButton(
                                onClick = {
                                    showManualConfirmDialog = false
                                    bypassStatus = "NORMAL"
                                }
                            ) {
                                Text("نعم، أكمل", color = Color(0xFFE50914))
                            }
                        },
                        dismissButton = {
                            androidx.compose.material3.TextButton(
                                onClick = { showManualConfirmDialog = false }
                            ) {
                                Text("إلغاء", color = Color.White)
                            }
                        }
                    )
                }

        // Hidden Extractor for Quality
        if (isExtractingQuality && selectedServerForQuality != null) {
            LaunchedEffect(selectedServerForQuality) {
                kotlinx.coroutines.delay(12000)
                if (isExtractingQuality && extractedQualities.isEmpty()) {
                    val serverUrl = extractedServerLinks[selectedServerForQuality] ?: finalWatchUrl ?: searchUrl
                    extractedQualities = listOf(com.example.utils.M3U8Parser.QualityInfo("جودة أصلية (Default)", serverUrl))
                    isExtractingQuality = false
                }
            }
            val serverUrl = extractedServerLinks[selectedServerForQuality] ?: finalWatchUrl ?: searchUrl
            HiddenVideoExtractor(
                url = serverUrl,
                isMovie = isMovie,
                season = season,
                episode = episode,
                targetServer = selectedServerForQuality,
                targetServerId = com.example.ui.screens.player.ServerStateStore.extractedServerIds[selectedServerForQuality],
                onVideoUrlFound = { url ->
                    if (url.contains(".m3u8")) {
                        coroutineScope.launch {
                            qualityExtractionMessage = "جاري تحليل الجودات..."
                            val qualities = com.example.utils.M3U8Parser.getQualities(url)
                            extractedQualities = qualities
                            isExtractingQuality = false
                        }
                    } else {
                        // Not an m3u8, just show default
                        extractedQualities = listOf(com.example.utils.M3U8Parser.QualityInfo("جودة أصلية (Default)", url))
                        isExtractingQuality = false
                    }
                },
                onIframeUrlFound = { iframeUrl ->
                    // Sometimes we get a new iframe url, we should probably follow it or just return it as quality
                    extractedQualities = listOf(com.example.utils.M3U8Parser.QualityInfo("جودة أصلية (Default)", iframeUrl))
                    isExtractingQuality = false
                }
            )
        }
        
        if (showCancelConfirmDialog) {
            AlertDialog(
                onDismissRequest = { showCancelConfirmDialog = false },
                containerColor = Color(0xFF222225),
                titleContentColor = Color.White,
                textContentColor = Color.LightGray,
                title = {
                    Text(text = "إلغاء العملية", fontWeight = FontWeight.Bold)
                },
                text = {
                    Text(text = "العملية لا تزال جارية، هل أنت متأكد أنك تريد الإلغاء؟")
                },
                confirmButton = {
                    TextButton(
                        onClick = {
                            showCancelConfirmDialog = false
                            onDismiss()
                        }
                    ) {
                        Text("نعم، إلغاء", color = Color(0xFFFF1111))
                    }
                },
                dismissButton = {
                    TextButton(
                        onClick = { showCancelConfirmDialog = false }
                    ) {
                        Text("متابعة", color = Color.White)
                    }
                }
            )
        }
    }
}

}
}

} 
@Composable
fun StatusBadge(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, statusColor: Color, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .clip(RoundedCornerShape(14.dp))
            .background(Color(0xFF19191C))
            .border(1.dp, Color(0xFF2C2C2E), RoundedCornerShape(14.dp))
            .padding(horizontal = 4.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Icon(icon, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(12.dp))
        Spacer(modifier = Modifier.width(2.dp))
        Text(text, color = Color.LightGray, fontSize = 9.sp, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
        Spacer(modifier = Modifier.width(2.dp))
        Box(modifier = Modifier.size(6.dp).background(statusColor, CircleShape))
}}
