with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

old_func = """    fun selectServer(serverName: String) {
        val servers = ServerStateStore.extractedServers
        val matchingServer = servers.find { it.name == serverName }
        if (matchingServer != null) {
            _uiState.value = _uiState.value.copy(
                currentServer = serverName,
                serverIdToChange = matchingServer.id,
                isLoading = true,
                extractionUrl = null
            )
            // Trigger recomposition/extraction in PlayerScreen by forcing URL reset
            val currentWatchUrl = _uiState.value.originalWatchUrl ?: return
            
            viewModelScope.launch {
                delay(100)
                _uiState.value = _uiState.value.copy(extractionUrl = currentWatchUrl, isLoading = true)
            }
        }
    }"""

new_func = """    fun selectServer(serverName: String) {
        val servers = ServerStateStore.extractedServers
        val matchingServer = servers.find { it.name == serverName }
        if (matchingServer != null) {
            _uiState.value = _uiState.value.copy(
                currentServer = serverName,
                serverIdToChange = matchingServer.id,
                isLoading = true,
                extractionUrl = null,
                currentVideoUrl = null,
                availableQualities = emptyList(),
                extractedQualitiesInfo = emptyList()
            )
            
            val currentWatchUrl = _uiState.value.originalWatchUrl ?: return
            
            viewModelScope.launch {
                delay(100)
                _uiState.value = _uiState.value.copy(extractionUrl = currentWatchUrl, isLoading = true)
            }
        }
    }"""

content = content.replace(old_func, new_func)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
