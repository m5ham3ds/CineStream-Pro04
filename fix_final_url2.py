import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

old_logic = """                val qualities = com.example.utils.M3U8Parser.getQualities(url)
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
                        currentVideoUrl = url,
                        isLoading = false
                    )"""

new_logic = """                val qualities = com.example.utils.M3U8Parser.getQualities(url)
                val serverName = _uiState.value.currentServer
                if (serverName.isNotEmpty()) {
                    com.example.ui.screens.player.ServerStateStore.serverQualities[serverName] = qualities
                }
                
                if (qualities.isNotEmpty()) {
                    val prevQualityName = _uiState.value.currentQuality
                    val targetQuality = if (qualities.find { it.name == prevQualityName } != null) {
                        qualities.find { it.name == prevQualityName }!!
                    } else if (prevQualityName == "Auto") {
                        val ctx = com.example.MyApplication.appContext
                        if (ctx != null) {
                            val bandwidth = com.example.utils.NetworkUtils.getEstimatedBandwidthKbps(ctx)
                            com.example.utils.NetworkUtils.selectBestQuality(qualities, bandwidth)
                        } else {
                            qualities.first()
                        }
                    } else {
                        qualities.first()
                    }
                    
                    val qualitiesWithAuto = listOf("Auto") + qualities.map { it.name }
                    
                    _uiState.value = _uiState.value.copy(
                        extractedQualitiesInfo = qualities,
                        availableQualities = qualitiesWithAuto,
                        currentQuality = if (prevQualityName == "Auto") "Auto" else targetQuality.name,
                        currentVideoUrl = url,
                        isLoading = false
                    )"""

content = content.replace(old_logic, new_logic)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
