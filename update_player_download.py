import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# Add downloadRepository and scope
if "val downloadRepository =" not in content:
    content = content.replace(
        "val context = LocalContext.current",
        "val context = LocalContext.current\n    val downloadRepository = remember { com.example.data.repository.DownloadRepository(context) }\n    val scope = rememberCoroutineScope()"
    )

# Replace the download logic
old_download = """                videoUrl?.let { url ->
                    com.example.utils.AndroidDownloader.downloadVideo(context, url, "${uiState.title} - $quality")
                } ?: run {
                    android.widget.Toast.makeText(context, "Please wait for the stream to load first.", android.widget.Toast.LENGTH_SHORT).show()
                }"""

new_download = """                videoUrl?.let { url ->
                    com.example.utils.AndroidDownloader.downloadVideo(context, url, "${uiState.title} - $quality")
                    scope.launch {
                        downloadRepository.addToDownloads(
                            com.example.data.model.DownloadItem(
                                id = "${uiState.title}_${System.currentTimeMillis()}",
                                title = "${uiState.title} - $quality",
                                posterUrl = uiState.posterUrl,
                                isMovie = uiState.isMovie,
                                progress = 0.05f,
                                isCompleted = false
                            )
                        )
                    }
                } ?: run {
                    android.widget.Toast.makeText(context, "Please wait for the stream to load first.", android.widget.Toast.LENGTH_SHORT).show()
                }"""

content = content.replace(old_download, new_download)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
