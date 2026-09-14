with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

new_select_server = """
    fun selectServer(server: String) {
        val link = _uiState.value.availableServerLinks[server]
        val id = _uiState.value.availableServerIds[server]
        
        val cachedQualities = com.example.ui.screens.player.ServerStateStore.serverQualities[server]
        if (cachedQualities != null && cachedQualities.isNotEmpty()) {
            val autoQuality = cachedQualities.firstOrNull()?.name ?: "Auto"
            val targetQuality = cachedQualities.find { it.name == _uiState.value.currentQuality } ?: cachedQualities.first()
            _uiState.value = _uiState.value.copy(
                currentServer = server,
                isLoading = false,
                currentVideoUrl = targetQuality.url,
                extractionUrl = null,
                serverIdToChange = id,
                extractedQualitiesInfo = cachedQualities,
                availableQualities = cachedQualities.map { it.name },
                currentQuality = targetQuality.name
            )
            return
        }

        var nextExtractionUrl = _uiState.value.extractionUrl
        if (link != null && link.isNotEmpty()) {
            nextExtractionUrl = link
        }
        
        _uiState.value = _uiState.value.copy(
            currentServer = server,
            isLoading = true,
            currentVideoUrl = null,
            extractionUrl = nextExtractionUrl,
            serverIdToChange = id
        )
        
        if (nextExtractionUrl != null) {
            if (nextExtractionUrl.contains(".m3u8") || nextExtractionUrl.contains(".mp4") || nextExtractionUrl.contains("akamaized.net")) {
                setFinalVideoUrl(nextExtractionUrl)
            } else {
                startExtractionTimeout()
            }
        } else {
            generateExtractionUrl()
        }
    }
"""

new_set_final = """
    fun setFinalVideoUrl(url: String) {
        extractionTimeoutJob?.cancel()
        
        viewModelScope.launch {
            try {
                val qualities = com.example.utils.M3U8Parser.getQualities(url)
                val serverName = _uiState.value.currentServer
                if (serverName.isNotEmpty()) {
                    com.example.ui.screens.player.ServerStateStore.serverQualities[serverName] = qualities
                }
                
                if (qualities.isNotEmpty()) {
                    // Try to keep the same quality (e.g. 1080p) or use the best
                    val prevQualityName = _uiState.value.currentQuality
                    val targetQuality = qualities.find { it.name == prevQualityName } ?: qualities.first()
                    
                    _uiState.value = _uiState.value.copy(
                        extractedQualitiesInfo = qualities,
                        availableQualities = qualities.map { it.name },
                        currentQuality = targetQuality.name,
                        currentVideoUrl = targetQuality.url,
                        isLoading = false
                    )
                } else {
                    _uiState.value = _uiState.value.copy(
                        currentVideoUrl = url,
                        isLoading = false
                    )
                }
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    currentVideoUrl = url,
                    isLoading = false
                )
            }
        }
    }
"""

# Replace selectServer
import re
content = re.sub(r'fun selectServer\(server: String\).*?fun selectEpisode', new_select_server.strip() + '\n\n    fun selectEpisode', content, flags=re.DOTALL)

# Replace setFinalVideoUrl
content = re.sub(r'fun setFinalVideoUrl\(url: String\).*?fun setIframeUrl', new_set_final.strip() + '\n\n    fun setIframeUrl', content, flags=re.DOTALL)

# Add imports
if "androidx.lifecycle.viewModelScope.launch" not in content:
    content = content.replace("import androidx.lifecycle.ViewModel", "import androidx.lifecycle.ViewModel\nimport kotlinx.coroutines.launch")

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)

print("Updated PlayerViewModel.kt")
