import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    c = f.read()

target1 = """fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, posterUrl: String = "", url: String? = null, targetServer: String? = null, website: String? = null, onBack: () -> Unit, viewModel: PlayerViewModel = viewModel()) {"""
replace1 = """fun PlayerScreen(mediaId: String, episodeId: String = "", isMovie: Boolean, title: String, posterUrl: String = "", url: String? = null, targetServer: String? = null, website: String? = null, onBack: () -> Unit, viewModel: PlayerViewModel = viewModel()) {"""
c = c.replace(target1, replace1)

# we need to check if the file is already downloading.
# We can observe the DB using getDownloadItemById

target2 = """    val downloadRepository = remember { com.example.data.repository.DownloadRepository(context) }
    val scope = rememberCoroutineScope()
    var showDownloadSheet by remember { mutableStateOf(false) }"""

replace2 = """    val downloadRepository = remember { com.example.data.repository.DownloadRepository(context) }
    val scope = rememberCoroutineScope()
    val fileId = if (isMovie) mediaId else "${mediaId}_${episodeId}"
    val downloadItem by downloadRepository.getDownloadItemById(fileId).collectAsState(initial = null)
    var showDownloadSheet by remember { mutableStateOf(false) }"""
c = c.replace(target2, replace2)

target3 = """                            BottomAction(icon = Icons.Default.Download, text = "Download") { showDownloadSheet = true }"""
replace3 = """                            BottomAction(icon = if (downloadItem?.isCompleted == true) Icons.Default.Check else Icons.Default.Download, text = if (downloadItem?.isCompleted == true) "Downloaded" else "Download") { 
                                if (downloadItem?.isCompleted == true) {
                                    android.widget.Toast.makeText(context, "Already downloaded", android.widget.Toast.LENGTH_SHORT).show()
                                } else if (downloadItem != null) {
                                    android.widget.Toast.makeText(context, "Already downloading", android.widget.Toast.LENGTH_SHORT).show()
                                } else {
                                    showDownloadSheet = true 
                                }
                            }"""
c = c.replace(target3, replace3)


target4 = """                videoUrl?.let { url ->
                    val fileId = "${uiState.mediaId}_${System.currentTimeMillis()}"
                    com.example.utils.AndroidDownloader.downloadVideo(context, url, "${fileId}.mp4", uiState.title)
                    scope.launch {
                        downloadRepository.addToDownloads(
                            com.example.data.model.DownloadItem(
                                id = fileId,
                                mediaId = uiState.mediaId,
                                title = uiState.title,
                                posterUrl = posterUrl,
                                isMovie = uiState.isMovie,
                                quality = "$quality||$url",
                                progress = 0.05f,
                                isCompleted = false
                            )
                        )
                    }
                } ?: run {"""

replace4 = """                videoUrl?.let { url ->
                    com.example.utils.AndroidDownloader.downloadVideo(context, url, fileId, uiState.title)
                    scope.launch {
                        downloadRepository.addToDownloads(
                            com.example.data.model.DownloadItem(
                                id = fileId,
                                mediaId = uiState.mediaId,
                                title = uiState.title,
                                posterUrl = posterUrl,
                                isMovie = uiState.isMovie,
                                quality = "$quality||$url",
                                progress = 0.05f,
                                isCompleted = false
                            )
                        )
                    }
                } ?: run {"""
c = c.replace(target4, replace4)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(c)
