import re

# Fix PlayerScreen
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

old_download_ps = """                    com.example.utils.AndroidDownloader.downloadVideo(context, url, "${uiState.title} - $quality")
                    scope.launch {
                        downloadRepository.addToDownloads(
                            com.example.data.model.DownloadItem(
                                id = "${uiState.title}_${System.currentTimeMillis()}",
                                title = uiState.title,
                                posterUrl = "",
                                isMovie = uiState.isMovie,
                                quality = quality,
                                progress = 0.05f,
                                isCompleted = false
                            )
                        )
                    }"""

new_download_ps = """                    val fileId = "${uiState.mediaId}_${System.currentTimeMillis()}"
                    com.example.utils.AndroidDownloader.downloadVideo(context, url, "${uiState.title} - $quality", fileId)
                    scope.launch {
                        downloadRepository.addToDownloads(
                            com.example.data.model.DownloadItem(
                                id = fileId,
                                mediaId = uiState.mediaId,
                                title = uiState.title,
                                posterUrl = "",
                                isMovie = uiState.isMovie,
                                quality = quality,
                                progress = 0.05f,
                                isCompleted = false
                            )
                        )
                    }"""
content = content.replace(old_download_ps, new_download_ps)
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)

# Fix DetailsScreens
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content2 = f.read()

# Movie download
old_movie_dl = """                                downloadRepository.addToDownloads(com.example.data.model.DownloadItem(
                                    id = movie.id, title = movie.originalTitle ?: movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = serverName
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, "${movie.title} - $serverName")"""

new_movie_dl = """                                downloadRepository.addToDownloads(com.example.data.model.DownloadItem(
                                    id = movie.id, mediaId = movie.id, title = movie.originalTitle ?: movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = serverName
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, "${movie.title} - $serverName", movie.id)"""
content2 = content2.replace(old_movie_dl, new_movie_dl)

# Series download
old_series_dl = """                                downloadRepository.addToDownloads(com.example.data.model.DownloadItem(
                                    id = series.id.toString(), title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false, quality = serverName
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, "$fullTitle - $serverName")"""

new_series_dl = """                                val epIdStr = "${series.id}_${ep.id}"
                                downloadRepository.addToDownloads(com.example.data.model.DownloadItem(
                                    id = epIdStr, mediaId = series.id.toString(), title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false, quality = serverName
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, "$fullTitle - $serverName", epIdStr)"""
content2 = content2.replace(old_series_dl, new_series_dl)

# Add downloadedItems tracking to DetailsScreens (Movies)
old_movie_repo = """    val isFavorite by libraryRepository.isItemInLibrary(movieId).collectAsState(initial = false)
    val downloadRepository = remember { DownloadRepository(context) }"""
new_movie_repo = """    val isFavorite by libraryRepository.isItemInLibrary(movieId).collectAsState(initial = false)
    val downloadRepository = remember { DownloadRepository(context) }
    val downloads by downloadRepository.getAllDownloads().collectAsState(initial = emptyList())
    val isDownloaded = downloads.any { it.id == movieId }"""
content2 = content2.replace(old_movie_repo, new_movie_repo)

old_movie_dl_btn = """                    IconButton(
                        onClick = { 
                            showSourceSheet = true 
                            isDownloadMode = true 
                        },
                        modifier = Modifier.size(50.dp).background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                    ) {
                        Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                    }"""
new_movie_dl_btn = """                    IconButton(
                        onClick = { 
                            showSourceSheet = true 
                            isDownloadMode = true 
                        },
                        modifier = Modifier.size(50.dp).background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                    ) {
                        if (isDownloaded) {
                            Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = Color.Green)
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                        }
                    }"""
content2 = content2.replace(old_movie_dl_btn, new_movie_dl_btn)

# Series downloaded items
old_series_repo = """    val isFavorite by libraryRepository.isItemInLibrary(seriesId).collectAsState(initial = false)
    val downloadRepository = remember { DownloadRepository(context) }"""
new_series_repo = """    val isFavorite by libraryRepository.isItemInLibrary(seriesId).collectAsState(initial = false)
    val downloadRepository = remember { DownloadRepository(context) }
    val downloads by downloadRepository.getAllDownloads().collectAsState(initial = emptyList())
    val downloadedEpisodeIds = downloads.map { it.id }.toSet()"""
content2 = content2.replace(old_series_repo, new_series_repo)

old_ep_card_call = """                        EpisodeCard(
                            episode = episode,
                            isWatched = isWatched,
                            onClick = {"""
new_ep_card_call = """                        val isDownloaded = downloadedEpisodeIds.contains("${series.id}_${episode.id}")
                        EpisodeCard(
                            episode = episode,
                            isWatched = isWatched,
                            isDownloaded = isDownloaded,
                            onClick = {"""
content2 = content2.replace(old_ep_card_call, new_ep_card_call)

old_ep_card_def = """fun EpisodeCard(
    episode: Episode,
    isWatched: Boolean,
    onClick: () -> Unit,"""
new_ep_card_def = """fun EpisodeCard(
    episode: Episode,
    isWatched: Boolean,
    isDownloaded: Boolean = false,
    onClick: () -> Unit,"""
content2 = content2.replace(old_ep_card_def, new_ep_card_def)

old_ep_card_dl_btn = """        IconButton(onClick = onDownloadClick) {
            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
        }"""
new_ep_card_dl_btn = """        IconButton(onClick = onDownloadClick) {
            if (isDownloaded) {
                Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = Color.Green)
            } else {
                Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
            }
        }"""
content2 = content2.replace(old_ep_card_dl_btn, new_ep_card_dl_btn)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content2)
