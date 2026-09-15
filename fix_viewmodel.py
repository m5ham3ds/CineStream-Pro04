import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

# Fix selectQuality to NOT change currentVideoUrl
old_select = """    fun selectQuality(qualityName: String) {
        val selectedQuality = _uiState.value.extractedQualitiesInfo.find { it.name == qualityName }
        if (selectedQuality != null) {
            _uiState.value = _uiState.value.copy(
                currentQuality = qualityName,
                currentVideoUrl = selectedQuality.url
            )
        } else {
            _uiState.value = _uiState.value.copy(
                currentQuality = qualityName
            )
        }
    }"""
new_select = """    fun selectQuality(qualityName: String) {
        _uiState.value = _uiState.value.copy(
            currentQuality = qualityName
        )
    }"""
content = content.replace(old_select, new_select)

# Fix selectServer to properly reset everything and use the extractionUrl
old_server = """        val cachedQualities = com.example.ui.screens.player.ServerStateStore.serverQualities[server]
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
        }"""
new_server = """        var nextExtractionUrl = _uiState.value.extractionUrl
        if (link != null && link.isNotEmpty()) {
            nextExtractionUrl = link
        }"""
content = content.replace(old_server, new_server)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
