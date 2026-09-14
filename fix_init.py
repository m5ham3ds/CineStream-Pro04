import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

new_init = """
        val targetServerName = targetServer ?: com.example.ui.screens.player.ServerStateStore.extractedServers.firstOrNull() ?: ""
        val qualitiesForServer = com.example.ui.screens.player.ServerStateStore.serverQualities[targetServerName] 
            ?: com.example.ui.screens.player.ServerStateStore.extractedQualities
            
        val matchedQuality = qualitiesForServer.find { it.url == directUrl } ?: qualitiesForServer.firstOrNull()

        _uiState.value = PlayerUiState(
            mediaId = mediaId,
            isMovie = isMovie,
            title = title,
            currentWebsite = website ?: com.example.ui.screens.player.ServerStateStore.extractedServers.firstOrNull() ?: "",
            fallbackWebsites = emptyList(), // we rely on what was found
            availableServers = com.example.ui.screens.player.ServerStateStore.extractedServers,
            availableServerLinks = com.example.ui.screens.player.ServerStateStore.extractedServerLinks,
            availableServerIds = com.example.ui.screens.player.ServerStateStore.extractedServerIds,
            currentServer = targetServerName,
            extractedQualitiesInfo = qualitiesForServer,
            availableQualities = if (qualitiesForServer.isNotEmpty()) {
                qualitiesForServer.map { it.name }
            } else {
                listOf("Auto")
            },
            currentQuality = matchedQuality?.name ?: "Auto"
        )
"""

content = re.sub(r'        _uiState\.value = PlayerUiState\(.*?\n        \)', new_init.strip(), content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)

print("Updated init logic")
