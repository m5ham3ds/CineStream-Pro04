import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    c = f.read()

target = """            if (watchUrl != null) {
                _uiState.value = _uiState.value.copy(extractionUrl = watchUrl, isLoading = true)
                startExtractionTimeout()
            } else {"""

replacement = """            if (watchUrl != null) {
                var finalUrl = watchUrl
                val currentServer = _uiState.value.currentServer
                if (currentServer.isNotEmpty()) {
                    val link = _uiState.value.availableServerLinks[currentServer]
                    if (link != null && link.isNotEmpty()) {
                        finalUrl = link
                    }
                }
                _uiState.value = _uiState.value.copy(extractionUrl = finalUrl, isLoading = true)
                startExtractionTimeout()
            } else {"""

c = c.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(c)
