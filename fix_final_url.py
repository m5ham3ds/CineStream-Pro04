import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

old_logic = """                    _uiState.value = _uiState.value.copy(
                        extractedQualitiesInfo = qualities,
                        availableQualities = qualities.map { it.name },
                        currentQuality = targetQuality.name,
                        currentVideoUrl = targetQuality.url,
                        isLoading = false
                    )"""

new_logic = """                    _uiState.value = _uiState.value.copy(
                        extractedQualitiesInfo = qualities,
                        availableQualities = qualities.map { it.name },
                        currentQuality = targetQuality.name,
                        currentVideoUrl = url,
                        isLoading = false
                    )"""

content = content.replace(old_logic, new_logic)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
