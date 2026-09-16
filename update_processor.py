import re

content = """package com.example.ui.components

import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.example.data.model.DownloadItem
import com.example.data.repository.DownloadRepository
import com.example.domain.models.Episode
import com.example.domain.models.Series
import com.example.extensions.ExtensionManager
import com.example.ui.screens.player.HiddenVideoExtractor
import com.example.ui.screens.player.ServerSelectionBridge
import com.example.utils.M3U8Parser
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

data class FinalDownloadData(
    val episodeId: String,
    val title: String,
    val posterUrl: String,
    val qualityName: String,
    val watchUrl: String
)

data class ExtractedServer(
    val name: String,
    val watchUrl: String
)

@Composable
fun BatchDownloadProcessor(
    series: Series,
    seasonNumber: Int,
    episodes: List<Episode>,
    targetQuality: String,
    onComplete: () -> Unit,
    onCancel: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val downloadRepository = remember { DownloadRepository(context) }
    
    val extensions = ExtensionManager.installedExtensions.collectAsState().value
    val currentExtension = extensions.firstOrNull()
    
    var currentIndex by remember { mutableIntStateOf(0) }
    var phase by remember { mutableStateOf("INIT") } 
    var statusMessage by remember { mutableStateOf("جاري التهيئة...") }
    
    var episodeServers by remember { mutableStateOf<List<ExtractedServer>>(emptyList()) }
    val finalDownloadList = remember { mutableStateListOf<FinalDownloadData>() }
    
    // Extraction State
    var activeExtractions by remember { mutableStateOf<List<ExtractedServer>>(emptyList()) }
    var nextServerIndex by remember { mutableIntStateOf(0) }
    var completedExtractions by remember { mutableIntStateOf(0) }
    var exactMatchFound by remember { mutableStateOf(false) }
    
    var bestFallbackUrl by remember { mutableStateOf<String?>(null) }
    var bestFallbackName by remember { mutableStateOf<String?>(null) }
    var bestFallbackScore by remember { mutableIntStateOf(-1) }

    fun moveToNextEpisode() {
        exactMatchFound = false
        activeExtractions = emptyList()
        episodeServers = emptyList()
        bestFallbackUrl = null
        bestFallbackName = null
        bestFallbackScore = -1
        currentIndex++
        phase = "INIT"
    }
    
    fun finishBatch() {
        scope.launch {
            statusMessage = "جاري بدء التنزيلات دفعة واحدة..."
            for (data in finalDownloadList) {
                val epIdStr = "${series.id}_${data.episodeId}"
                downloadRepository.addToDownloads(DownloadItem(
                    id = epIdStr, mediaId = series.id.toString(), title = data.title, posterUrl = data.posterUrl, isMovie = false, quality = "${data.qualityName}||${data.watchUrl}"
                ))
                com.example.utils.AndroidDownloader.downloadVideo(context, data.watchUrl, epIdStr, "${data.title} - ${data.qualityName}")
            }
            delay(1500)
            onComplete()
        }
    }

    LaunchedEffect(currentIndex, phase) {
        if (currentIndex >= episodes.size) {
            if (phase != "DONE") {
                phase = "DONE"
                finishBatch()
            }
            return@LaunchedEffect
        }
        
        if (currentExtension == null) {
            statusMessage = "لا يوجد إضافات متوفرة"
            delay(1500)
            onCancel()
            return@LaunchedEffect
        }

        val episode = episodes[currentIndex]
        
        if (phase == "INIT") {
            statusMessage = "جاري تجهيز بيانات الحلقة ${episode.episodeNumber}..."
            delay(500)
            phase = "GETTING_SERVERS"
        }
        
        if (phase == "GETTING_SERVERS") {
            val timeoutPhase = phase
            val timeoutIndex = currentIndex
            delay(15000) 
            if (phase == timeoutPhase && currentIndex == timeoutIndex) {
                moveToNextEpisode()
            }
        }
        
        if (phase == "BATCH_EXTRACTING") {
            val timeoutPhase = phase
            val timeoutIndex = currentIndex
            delay(60000) // 60 seconds total for extracting all servers for one episode
            if (phase == timeoutPhase && currentIndex == timeoutIndex) {
                // Force proceed with best fallback
                if (bestFallbackUrl != null && !exactMatchFound) {
                    exactMatchFound = true // prevent further updates
                    val rawTitle = series.originalTitle ?: series.title
                    val fullTitle = "$rawTitle - S${seasonNumber}E${episode.episodeNumber}"
                    finalDownloadList.add(FinalDownloadData(episode.id, fullTitle, episode.thumbnailUrl, bestFallbackName ?: "Default", bestFallbackUrl!!))
                }
                moveToNextEpisode()
            }
        }
    }
    
    fun handleServerExtracted(server: ExtractedServer, q: List<M3U8Parser.QualityInfo>, extractedUrl: String) {
        if (exactMatchFound) return
        
        val sortedQ = q.sortedByDescending { it.name.replace("p", "").toIntOrNull() ?: 0 }
        
        var foundUrl = extractedUrl
        var foundName = "Default"
        var foundScore = 0
        var isExact = false
        
        if (targetQuality == "Auto" || targetQuality.isEmpty()) {
            if (sortedQ.isNotEmpty()) {
                foundUrl = sortedQ.first().url
                foundName = "${server.name} - ${sortedQ.first().name}"
                foundScore = 9999
                isExact = true // Auto is always exact match on first server
            } else {
                foundName = "${server.name} - Default"
                foundScore = 1
                isExact = true
            }
        } else {
            val targetHeight = targetQuality.replace("p", "").toIntOrNull() ?: 0
            val exactMatch = sortedQ.find { it.name.contains(targetQuality.replace("p", "")) }
            if (exactMatch != null) {
                foundUrl = exactMatch.url
                foundName = "${server.name} - ${exactMatch.name}"
                foundScore = targetHeight
                isExact = true
            } else if (sortedQ.isNotEmpty()) {
                val closest = sortedQ.find { (it.name.replace("p", "").toIntOrNull() ?: 0) <= targetHeight }
                if (closest != null) {
                    foundUrl = closest.url
                    foundName = "${server.name} - ${closest.name}"
                    foundScore = closest.name.replace("p", "").toIntOrNull() ?: 0
                } else {
                    foundUrl = sortedQ.last().url
                    foundName = "${server.name} - ${sortedQ.last().name}"
                    foundScore = sortedQ.last().name.replace("p", "").toIntOrNull() ?: 0
                }
            } else {
                foundName = "${server.name} - Default"
                foundScore = 0
            }
        }
        
        if (isExact) {
            exactMatchFound = true
            val episode = episodes[currentIndex]
            val rawTitle = series.originalTitle ?: series.title
            val fullTitle = "$rawTitle - S${seasonNumber}E${episode.episodeNumber}"
            finalDownloadList.add(FinalDownloadData(episode.id, fullTitle, episode.thumbnailUrl, foundName, foundUrl))
            moveToNextEpisode()
        } else {
            if (foundScore > bestFallbackScore) {
                bestFallbackScore = foundScore
                bestFallbackUrl = foundUrl
                bestFallbackName = foundName
            }
            
            completedExtractions++
            activeExtractions = activeExtractions.filter { it.name != server.name }
            
            if (nextServerIndex < episodeServers.size) {
                activeExtractions = activeExtractions + episodeServers[nextServerIndex]
                nextServerIndex++
            } else if (activeExtractions.isEmpty()) {
                // All servers checked, use best fallback
                if (bestFallbackUrl != null && !exactMatchFound) {
                    exactMatchFound = true
                    val episode = episodes[currentIndex]
                    val rawTitle = series.originalTitle ?: series.title
                    val fullTitle = "$rawTitle - S${seasonNumber}E${episode.episodeNumber}"
                    finalDownloadList.add(FinalDownloadData(episode.id, fullTitle, episode.thumbnailUrl, bestFallbackName ?: "Default", bestFallbackUrl!!))
                }
                moveToNextEpisode()
            }
        }
    }
    
    // UI Dialog
    AlertDialog(
        onDismissRequest = {}, 
        title = { Text("التحميل الجماعي") },
        text = {
            Column(
                modifier = Modifier.fillMaxWidth(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                CircularProgressIndicator()
                Text(statusMessage)
                if (phase != "DONE") {
                    Text("${currentIndex + 1} / ${episodes.size}")
                }
            }
        },
        confirmButton = {
            TextButton(onClick = onCancel) {
                Text("إلغاء")
            }
        }
    )

    Box(modifier = Modifier.size(1.dp).clip(RoundedCornerShape(1.dp))) {
        if (phase == "GETTING_SERVERS" && currentIndex < episodes.size && currentExtension != null) {
            val episode = episodes[currentIndex]
            val rawTitle = series.originalTitle ?: series.title
            val baseTitle = if (rawTitle.contains(" - S") && rawTitle.contains("E")) {
                rawTitle.substringBefore(" - S").trim()
            } else rawTitle
            val year = series.year.toString()
            val cleanTitleWithYear = if (year.isNotBlank() && year != "0") {
                "$baseTitle $year".replace(Regex("[^a-zA-Z0-9\\\\s]"), " ").replace(Regex("\\\\s+"), " ").trim()
            } else {
                baseTitle.replace(Regex("[^a-zA-Z0-9\\\\s]"), " ").replace(Regex("\\\\s+"), " ").trim()
            }
            
            val htmlData = \"\"\"
                <html>
                <head>
                    <script>
                        ${currentExtension.getExtractionScript(isMovie = false, episode = episode.episodeNumber, title = cleanTitleWithYear)}
                    </script>
                </head>
                <body></body>
                </html>
            \"\"\".trimIndent()
            
            AndroidView(
                factory = { ctx ->
                    WebView(ctx).apply {
                        settings.javaScriptEnabled = true
                        settings.domStorageEnabled = true
                        val bridge = ServerSelectionBridge(
                            onLogDebug = {},
                            onSendBypassStatus = {},
                            onSendFailed = {
                                android.os.Handler(android.os.Looper.getMainLooper()).post {
                                    moveToNextEpisode()
                                }
                            },
                            onSendServers = { _, _ -> },
                            onSendServersV2 = { serversJson, _ ->
                                android.os.Handler(android.os.Looper.getMainLooper()).post {
                                    try {
                                        val serversData = org.json.JSONArray(serversJson)
                                        val serversNames = mutableListOf<String>()
                                        val serversMap = mutableMapOf<String, String>()
                                        val downloadsMap = mutableMapOf<String, String>()
                                        
                                        for (i in 0 until serversData.length()) {
                                            val item = serversData.getJSONObject(i)
                                            val name = item.getString("name")
                                            val link = if (item.has("link")) item.getString("link") else if (item.has("url")) item.getString("url") else ""
                                            if (name.contains("(تحميل)") || link.endsWith(".mp4") || link.endsWith(".mkv")) {
                                                downloadsMap[name] = link
                                            } else {
                                                serversNames.add(name)
                                                serversMap[name] = link
                                            }
                                        }
                                        
                                        val extractedList = mutableListOf<ExtractedServer>()
                                        for (sName in serversNames) {
                                            val finalUrl = serversMap[sName] ?: ""
                                            val dLink = downloadsMap[sName] ?: ""
                                            val watchUrl = if (finalUrl.contains("akamaized.net") || finalUrl.endsWith(".m3u8") || finalUrl.endsWith(".mp4")) {
                                                finalUrl
                                            } else if (dLink.isNotEmpty()) {
                                                dLink
                                            } else {
                                                finalUrl
                                            }
                                            extractedList.add(ExtractedServer(sName, watchUrl))
                                        }
                                        
                                        if (extractedList.isNotEmpty()) {
                                            episodeServers = extractedList
                                            nextServerIndex = minOf(3, extractedList.size)
                                            activeExtractions = extractedList.take(3)
                                            completedExtractions = 0
                                            exactMatchFound = false
                                            phase = "BATCH_EXTRACTING"
                                            statusMessage = "جاري البحث عن الجودة في السيرفرات..."
                                        } else {
                                            moveToNextEpisode()
                                        }
                                    } catch (e: Exception) {
                                        moveToNextEpisode()
                                    }
                                }
                            }
                        )
                        addJavascriptInterface(bridge, "Android")
                        webViewClient = object : WebViewClient() {}
                    }
                },
                update = { webView ->
                    webView.loadDataWithBaseURL(currentExtension.baseUrl, htmlData, "text/html", "UTF-8", null)
                }
            )
        }
        
        if (phase == "BATCH_EXTRACTING") {
            for (server in activeExtractions) {
                var isMp4 = false
                if (server.watchUrl.contains(".mp4") && !server.watchUrl.contains(".m3u8")) {
                    isMp4 = true
                }
                
                if (isMp4) {
                    LaunchedEffect(server.name) {
                        handleServerExtracted(server, emptyList(), server.watchUrl)
                    }
                } else {
                    HiddenVideoExtractor(
                        url = server.watchUrl,
                        isMovie = false,
                        season = seasonNumber,
                        episode = episodes[currentIndex].episodeNumber,
                        onVideoUrlFound = { extractedUrl ->
                            scope.launch {
                                val q = M3U8Parser.getQualities(extractedUrl)
                                handleServerExtracted(server, q, extractedUrl)
                            }
                        },
                        onIframeUrlFound = { }, // Ignored in batch, stick to watchUrl
                        onExtractionFailed = {
                            scope.launch {
                                handleServerExtracted(server, emptyList(), server.watchUrl) // act as default
                            }
                        }
                    )
                }
            }
        }
    }
}
"""

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "w") as f:
    f.write(content)

