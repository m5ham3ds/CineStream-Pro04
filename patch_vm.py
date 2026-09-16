with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

target = """        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            isAnime = isAnime,
            title = initialTitle,
            availableWebsites = com.example.extensions.ExtensionManager.installedExtensions.value.map { it.name },
            currentWebsite = bestWebsite,
            fallbackWebsites = remainingFallbacks,
            currentServer = targetServer ?: "",
            availableServers = com.example.ui.screens.player.ServerStateStore.extractedServers,
            availableServerLinks = com.example.ui.screens.player.ServerStateStore.extractedServerLinks,
            availableServerIds = com.example.ui.screens.player.ServerStateStore.extractedServerIds,
            extractedQualitiesInfo = com.example.ui.screens.player.ServerStateStore.extractedQualities,"""

replacement = """        val serverIds = com.example.ui.screens.player.ServerStateStore.extractedServerIds

        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            isAnime = isAnime,
            title = initialTitle,
            availableWebsites = com.example.extensions.ExtensionManager.installedExtensions.value.map { it.name },
            currentWebsite = bestWebsite,
            fallbackWebsites = remainingFallbacks,
            currentServer = targetServer ?: "",
            availableServers = com.example.ui.screens.player.ServerStateStore.extractedServers,
            availableServerLinks = com.example.ui.screens.player.ServerStateStore.extractedServerLinks,
            availableServerIds = serverIds,
            serverIdToChange = if (targetServer != null) serverIds[targetServer] else null,
            extractedQualitiesInfo = com.example.ui.screens.player.ServerStateStore.extractedQualities,"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
