import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Update EpisodeCard signature
content = content.replace(
    "isDownloaded: Boolean = false,",
    "downloadItem: com.example.data.model.DownloadItem? = null,"
)

# Update EpisodeCard implementation
old_dl_icon = """        IconButton(onClick = onDownloadClick) {
            if (isDownloaded) {
                Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = Color.Green)
            } else {
                Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
            }
        }"""
new_dl_icon = """        IconButton(onClick = onDownloadClick) {
            if (downloadItem?.isCompleted == true) {
                Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = MaterialTheme.colorScheme.primary)
            } else if (downloadItem != null) {
                AnimatedDownloadIcon(isPaused = downloadItem.isPaused)
            } else {
                Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
            }
        }"""
content = content.replace(old_dl_icon, new_dl_icon)

# Update EpisodeCard usages
old_usage = """                        val isDownloaded = downloadedEpisodeIds.contains("${series.id}_${episode.id}")
                        EpisodeCard(
                            episode = episode,
                            isWatched = isWatched,
                            isDownloaded = isDownloaded,
                            onClick = {"""

new_usage = """                        val downloadItem = downloads.find { it.id == "${series.id}_${episode.id}" }
                        val isDownloaded = downloadItem?.isCompleted == true
                        EpisodeCard(
                            episode = episode,
                            isWatched = isWatched,
                            downloadItem = downloadItem,
                            onClick = {"""
content = content.replace(old_usage, new_usage)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
