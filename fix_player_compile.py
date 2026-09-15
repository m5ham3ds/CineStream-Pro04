import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# 1. Add isBuffering
if "var isBuffering" not in content:
    content = content.replace("var isPlaying by remember { mutableStateOf(false) }", "var isPlaying by remember { mutableStateOf(false) }\n    var isBuffering by remember { mutableStateOf(true) }")

# 2. Fix scope.launch missing import or unresolved
# I will just import kotlinx.coroutines.launch at the top
if "import kotlinx.coroutines.launch" not in content:
    content = content.replace("import kotlinx.coroutines.delay", "import kotlinx.coroutines.delay\nimport kotlinx.coroutines.launch")

# 3. Fix DownloadItem initialization in PlayerScreen
old_download_item = """                        downloadRepository.addToDownloads(
                            com.example.data.model.DownloadItem(
                                id = "${uiState.title}_${System.currentTimeMillis()}",
                                title = "${uiState.title} - $quality",
                                posterUrl = uiState.posterUrl,
                                isMovie = uiState.isMovie,
                                progress = 0.05f,
                                isCompleted = false
                            )
                        )"""

new_download_item = """                        downloadRepository.addToDownloads(
                            com.example.data.model.DownloadItem(
                                id = "${uiState.title}_${System.currentTimeMillis()}",
                                title = uiState.title,
                                posterUrl = "",
                                isMovie = uiState.isMovie,
                                quality = quality,
                                progress = 0.05f,
                                isCompleted = false
                            )
                        )"""

content = content.replace(old_download_item, new_download_item)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
