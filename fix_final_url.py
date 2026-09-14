import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

new_set_final = """
    fun setFinalVideoUrl(url: String) {
        extractionTimeoutJob?.cancel()
        
        // Immediately stop extraction to prevent multiple calls
        _uiState.value = _uiState.value.copy(extractionUrl = null)
        
        viewModelScope.launch {
            try {
                val qualities = com.example.utils.M3U8Parser.getQualities(url)
                val serverName = _uiState.value.currentServer
                if (serverName.isNotEmpty()) {
                    com.example.ui.screens.player.ServerStateStore.serverQualities[serverName] = qualities
                }
                
                if (qualities.isNotEmpty()) {
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

content = re.sub(r'    fun setFinalVideoUrl\(url: String\).*?        \}\n    \}', new_set_final.strip(), content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)

print("Updated setFinalVideoUrl")
