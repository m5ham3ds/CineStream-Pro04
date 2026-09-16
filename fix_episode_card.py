import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

target1 = """    onLongClick: () -> Unit,
    onDownloadClick: () -> Unit
) {"""

replace1 = """    onLongClick: () -> Unit,
    onDownloadClick: () -> Unit,
    onLongDownloadClick: () -> Unit = {}
) {"""

c = c.replace(target1, replace1)

target2 = """        IconButton(onClick = onDownloadClick) {
            if (downloadItem?.isCompleted == true) {
                Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = MaterialTheme.colorScheme.primary)
            } else if (downloadItem != null) {
                AnimatedDownloadIcon(isPaused = downloadItem.isPaused)
            } else {
                Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
            }
        }"""

replace2 = """        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .combinedClickable(
                    onClick = onDownloadClick,
                    onLongClick = onLongDownloadClick
                ),
            contentAlignment = Alignment.Center
        ) {
            if (downloadItem?.isCompleted == true) {
                Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = MaterialTheme.colorScheme.primary)
            } else if (downloadItem != null) {
                AnimatedDownloadIcon(isPaused = downloadItem.isPaused)
            } else {
                Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
            }
        }"""

c = c.replace(target2, replace2)

# Update SeriesDetails calling EpisodeCard
# Find where EpisodeCard is called (around line 680)

# We need to add logic to onDownloadClick for Series
# wait, currently SeriesDetails does:
#                            onDownloadClick = {
#                                if (downloadItem?.isCompleted == true) {
#                                    scope.launch { downloadRepository.removeFromDownloads(downloadItem) }
#                                } else if (downloadItem != null) {
#                                    scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
#                                } else {

target3 = """                            onDownloadClick = {
                                if (downloadItem?.isCompleted == true) {
                                    scope.launch { downloadRepository.removeFromDownloads(downloadItem) }
                                } else if (downloadItem != null) {
                                    scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
                                } else {"""

replace3 = """                            onDownloadClick = {
                                if (downloadItem?.isCompleted == true) {
                                    Toast.makeText(context, "Already downloaded", Toast.LENGTH_SHORT).show()
                                } else if (downloadItem != null) {
                                    val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                                        action = if (downloadItem.isPaused) "RESUME" else "PAUSE"
                                        putExtra("id", "${series.id}_${episode.id}")
                                    }
                                    context.startService(intent)
                                    scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
                                    Toast.makeText(context, if (downloadItem.isPaused) "Resumed" else "Paused", Toast.LENGTH_SHORT).show()
                                } else {"""
c = c.replace(target3, replace3)

# And add onLongDownloadClick for SeriesDetails

target4 = """                            },
                            onDownloadClick = {"""
                            
replace4 = """                            },
                            onLongDownloadClick = {
                                if (downloadItem != null && !downloadItem.isCompleted) {
                                    // we can reuse the same delete confirmation but we need a state for episode delete
                                    val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                                        action = "CANCEL"
                                        putExtra("id", "${series.id}_${episode.id}")
                                    }
                                    context.startService(intent)
                                    scope.launch { downloadRepository.removeFromDownloads(downloadItem) }
                                    Toast.makeText(context, "Download cancelled", Toast.LENGTH_SHORT).show()
                                }
                            },
                            onDownloadClick = {"""
c = c.replace(target4, replace4)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)
