package com.example.ui.screens.player

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.background
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.ui.res.stringResource
import com.example.R
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.ui.unit.IntOffset
import kotlin.math.roundToInt
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import androidx.compose.ui.viewinterop.AndroidView

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun HiddenVideoExtractor(
    url: String,
    isMovie: Boolean = true,
    season: Int = 1,
    episode: Int = 1,
    targetServer: String? = null,
    targetServerId: String? = null,
    website: String = "",
    title: String = "",
    onVideoUrlFound: (String) -> Unit,
    onIframeUrlFound: ((String) -> Unit)? = null,
    onServersFound: ((List<String>) -> Unit)? = null, onExtractionFailed: (() -> Unit)? = null,
    onCloudflareDetected: ((Boolean) -> Unit)? = null
) {
    var isCloudflareDetected by remember { mutableStateOf(false) }
    var showConfirmDialog by remember { mutableStateOf(false) }
    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }

    if (showConfirmDialog) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { showConfirmDialog = false },
            title = { Text(stringResource(R.string.confirm)) },
            text = { Text(stringResource(R.string.confirm_cf)) },
            confirmButton = {
                androidx.compose.material3.TextButton(
                    onClick = {
                        showConfirmDialog = false
                        isCloudflareDetected = false
                        onCloudflareDetected?.invoke(false)
                    }
                ) {
                    Text(stringResource(R.string.yes_continue))
                }
            },
            dismissButton = {
                androidx.compose.material3.TextButton(
                    onClick = { showConfirmDialog = false }
                ) {
                    Text(stringResource(R.string.cancel_ar))
                }
            }
        )
    }

    Box(
        modifier = if (isCloudflareDetected) Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background.copy(alpha = 0.8f))
            .zIndex(100f)
        else Modifier.size(1.dp).alpha(0f),
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = if (isCloudflareDetected) Modifier
                .offset { IntOffset(offsetX.roundToInt(), offsetY.roundToInt()) }
                .pointerInput(Unit) {
                    detectDragGestures { change, dragAmount ->
                        change.consume()
                        offsetX += dragAmount.x
                        offsetY += dragAmount.y
                    }
                }
                .fillMaxWidth(0.9f)
                .fillMaxHeight(0.8f)
                .clip(RoundedCornerShape(16.dp))
                .background(MaterialTheme.colorScheme.onBackground)
            else Modifier.fillMaxSize()
        ) {
            Column(modifier = Modifier.fillMaxSize()) {
                if (isCloudflareDetected) {
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
                            showConfirmDialog = true
                        },
                        modifier = Modifier
                            .padding(horizontal = 16.dp, vertical = 8.dp)
                            .fillMaxWidth()
                    ) {
                        Text(stringResource(R.string.verified_continue))
                    }
                }
                AndroidView(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    factory = { ctx ->
            WebView(ctx).apply {
                setInitialScale(1)
                settings.apply {
                    javaScriptEnabled = true
                    domStorageEnabled = true
                    databaseEnabled = true
                    javaScriptCanOpenWindowsAutomatically = true
                    mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                    cacheMode = WebSettings.LOAD_DEFAULT
                    // This is critical: force media to auto-play so we can catch the network request
                    mediaPlaybackRequiresUserGesture = false 
                    
                    // Spoofing settings to look like real Chrome
                    val originalUserAgent = WebSettings.getDefaultUserAgent(ctx)
                    userAgentString = originalUserAgent.replace("; wv", "").replace("Version/4.0 ", "")
                    setSupportZoom(true)
                    builtInZoomControls = true
                    displayZoomControls = false
                    useWideViewPort = true
                    loadWithOverviewMode = true
                    allowFileAccess = true
                    allowContentAccess = true
                }

                val cookieManager = CookieManager.getInstance()
                cookieManager.setAcceptCookie(true)
                cookieManager.setAcceptThirdPartyCookies(this, true)

                
                val bridge = VideoExtractorBridge(
                    onSendServers = { serversStr ->
                        val servers = serversStr.split(",").filter { it.isNotBlank() }
                        if (servers.isNotEmpty()) {
                            Handler(Looper.getMainLooper()).post {
                                onServersFound?.invoke(servers)
                            }
                        }
                    },
                    onSendServersV2 = { serversJson, url ->
                        try {
                            val serversData = org.json.JSONArray(serversJson)
                            val serversNames = mutableListOf<String>()
                            val serversMap = mutableMapOf<String, String>()
                            val serversIds = mutableMapOf<String, String>()
                            
                            for (i in 0 until serversData.length()) {
                                val item = serversData.getJSONObject(i)
                                val name = item.getString("name")
                                val link = if (item.has("link")) item.getString("link") else ""
                                val id = if (item.has("id")) item.getString("id") else ""
                                serversNames.add(name)
                                serversMap[name] = link
                                serversIds[name] = id
                            }
                            
                            if (serversNames.isNotEmpty()) {
                                Handler(Looper.getMainLooper()).post {
                                    com.example.ui.screens.player.ServerStateStore.extractedServers = serversNames
                                    com.example.ui.screens.player.ServerStateStore.extractedServerLinks = serversMap
                                    com.example.ui.screens.player.ServerStateStore.extractedServerIds = serversIds
                                    onServersFound?.invoke(serversNames)
                                }
                            }
                        } catch (e: Exception) { e.printStackTrace() }
                    },
                    onSendIframeUrl = { url ->
                        Handler(Looper.getMainLooper()).post {
                            onIframeUrlFound?.invoke(url) ?: onVideoUrlFound(url)
                        }
                    },
                    onSendVideoUrl = { url ->
                        Handler(Looper.getMainLooper()).post {
                            onVideoUrlFound(url)
                        }
                    },
                    onSendFailed = {
                        Handler(Looper.getMainLooper()).post { onExtractionFailed?.invoke() }
                    },
                    onSendBypassStatus = { status ->
                        Handler(Looper.getMainLooper()).post {
                            val isCf = (status == "CLOUDFLARE")
                            isCloudflareDetected = isCf
                            onCloudflareDetected?.invoke(isCf)
                        }
                    }
                )
                addJavascriptInterface(bridge, "AndroidBridge")


                webViewClient = object : WebViewClient() {
                    var found = false

                    override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                        handler?.proceed()
                    }

                    override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                        found = false
                                                // Spoof navigator properties to evade bot detection
                        view?.evaluateJavascript("""
                            Object.defineProperty(navigator, 'webdriver', { get: () => false });
                            Object.defineProperty(navigator, 'languages', { get: () => ['ar', 'en-US', 'en'] });
                            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                            window.chrome = { runtime: {} };
                        """.trimIndent(), null)
                        super.onPageStarted(view, url, favicon)
                    }

                    override fun shouldInterceptRequest(
                        view: WebView?,
                        request: WebResourceRequest?
                    ): WebResourceResponse? {
                        val reqUrl = request?.url.toString()
                        
                        // Look for standard streaming formats
                        if (!found && (reqUrl.contains(".m3u8") || reqUrl.contains(".mp4") || reqUrl.contains(".mkv") || reqUrl.contains("videodelivery.net") || reqUrl.contains("v.mp4"))) {
                            // Avoid common ad scripts that might have these strings
                            if (!reqUrl.contains("adsystem") && !reqUrl.contains("tracker") && !reqUrl.contains("googleads") && !reqUrl.contains("facebook") && !reqUrl.contains("tiktok")) {
                                found = true
                                Handler(Looper.getMainLooper()).post {
                                    onVideoUrlFound(reqUrl)
                                }
                            }
                        }
                        
                        return super.shouldInterceptRequest(view, request)
                    }

                    override fun onPageFinished(view: WebView, url: String) {
                        super.onPageFinished(view, url)
                                                
                        fun injectScript() {
                            if (found) return
                            if (com.example.ui.screens.player.ServerStateStore.extractedServers.isEmpty()) {
                                val siteScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(
                                    website, 
                                    isMovie, 
                                    episode, 
                                    title
                                )
                                view.evaluateJavascript(siteScript, null)
                            } else {
                                val currentTargetServerId = view.getTag(com.example.R.id.tag_server_id) as? String ?: targetServerId
                                val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url, currentTargetServerId)
                                view.evaluateJavascript(autoPlayScript, null)
                            }
                        }
                        
                        injectScript()
                        
                        // Hybrid polling: keep injecting every 1.5s for up to 15s in case of AJAX loading
                        for (i in 1..10) {
                            Handler(Looper.getMainLooper()).postDelayed({
                                injectScript()
                            }, i * 1500L)
                        }
                    }
                }
            }
        },
        onRelease = { webView ->
            webView.stopLoading()
            webView.destroy()
        },
        update = { webView ->
            // Use getTag to store the original loaded url to avoid reloading when webView.url changes due to internal navigation
            val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String
            val lastServer = webView.getTag(com.example.R.id.tag_server) as? String

            if (lastUrl != url) {
                webView.setTag(com.example.R.id.tag_url, url)
                webView.setTag(com.example.R.id.tag_server, targetServer)
                webView.setTag(com.example.R.id.tag_server_id, targetServerId)
                val extraHeaders = mutableMapOf<String, String>()
                extraHeaders["Accept-Language"] = "ar,en-US;q=0.9,en;q=0.8"
                extraHeaders["DNT"] = "1"
                extraHeaders["Upgrade-Insecure-Requests"] = "1"
                extraHeaders["Sec-Fetch-Dest"] = "document"
                extraHeaders["Sec-Fetch-Mode"] = "navigate"
                extraHeaders["Sec-Fetch-Site"] = "none"
                extraHeaders["Sec-Fetch-User"] = "?1"
                webView.loadUrl(url, extraHeaders)
            } else if (lastServer != targetServer) {
                webView.setTag(com.example.R.id.tag_server, targetServer)
                webView.setTag(com.example.R.id.tag_server_id, targetServerId)
                webView.reload() // Server changed, reload the page
            }
        }
    )
            }
        }
    }
}

class VideoExtractorBridge(
    private val onSendServers: (String) -> Unit,
    private val onSendServersV2: (String, String) -> Unit,
    private val onSendIframeUrl: (String) -> Unit,
    private val onSendVideoUrl: (String) -> Unit,
    private val onSendFailed: () -> Unit,
    private val onSendBypassStatus: (String) -> Unit
) {
    @android.webkit.JavascriptInterface
    fun sendServers(serversStr: String) { onSendServers(serversStr) }

    @android.webkit.JavascriptInterface
    fun sendServersV2(serversJson: String, url: String) { onSendServersV2(serversJson, url) }

    @android.webkit.JavascriptInterface
    fun sendIframeUrl(url: String) { onSendIframeUrl(url) }

    @android.webkit.JavascriptInterface
    fun sendVideoUrl(url: String) { onSendVideoUrl(url) }

    @android.webkit.JavascriptInterface
    fun sendFailed() { onSendFailed() }

    @android.webkit.JavascriptInterface
    fun sendBypassStatus(status: String) { onSendBypassStatus(status) }
}