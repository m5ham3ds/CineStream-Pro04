import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

# Add OptIn and ExperimentalFoundationApi to imports if not there
if "import androidx.compose.foundation.ExperimentalFoundationApi" not in c:
    c = c.replace('import androidx.compose.foundation.layout.*', 'import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.ExperimentalFoundationApi\nimport androidx.compose.foundation.combinedClickable')

if "@OptIn(ExperimentalFoundationApi::class)" not in c:
    c = c.replace('@Composable\nfun DetailsScreen', '@OptIn(ExperimentalFoundationApi::class)\n@Composable\nfun DetailsScreen')
    c = c.replace('@Composable\nfun SeriesDetails', '@OptIn(ExperimentalFoundationApi::class)\n@Composable\nfun SeriesDetails')
    c = c.replace('@Composable\nfun EpisodeItem', '@OptIn(ExperimentalFoundationApi::class)\n@Composable\nfun EpisodeItem')

# --- Fix Movie Download Button ---
movie_btn_target = """                    IconButton(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                showDeleteConfirm = true
                            } else if (downloadItem != null) {
                                scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
                            } else {
                                isDownloadMode = true
                                if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                    showNoExtensionsDialog = true
                                } else {
                                    showSourceSheet = true
                                }
                            }
                        },
                        modifier = Modifier.size(50.dp).background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                    ) {"""

movie_btn_replace = """                    Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier
                            .size(50.dp)
                            .background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                            .clip(CircleShape)
                            .combinedClickable(
                                onClick = { 
                                    if (downloadItem?.isCompleted == true) {
                                        Toast.makeText(context, "Already downloaded", Toast.LENGTH_SHORT).show()
                                    } else if (downloadItem != null) {
                                        val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                                            action = if (downloadItem.isPaused) "RESUME" else "PAUSE"
                                            putExtra("id", movie.id.toString())
                                        }
                                        context.startService(intent)
                                        scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
                                        Toast.makeText(context, if (downloadItem.isPaused) "Resumed" else "Paused", Toast.LENGTH_SHORT).show()
                                    } else {
                                        isDownloadMode = true
                                        if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                            showNoExtensionsDialog = true
                                        } else {
                                            showSourceSheet = true
                                        }
                                    }
                                },
                                onLongClick = {
                                    if (downloadItem != null && !downloadItem.isCompleted) {
                                        showDeleteConfirm = true
                                    }
                                }
                            )
                    ) {"""
c = c.replace(movie_btn_target, movie_btn_replace)

# We need a delete confirmation dialog for active downloads. We can reuse showDeleteConfirm but it will delete the completed file too.
# Let's adjust the showDeleteConfirm dialog for the movie.

movie_dialog_target = """        if (showDeleteConfirm && downloadItem != null) {
            AlertDialog(
                onDismissRequest = { showDeleteConfirm = false },
                title = { Text(stringResource(R.string.delete_download_title, movie.title)) },
                text = { Text(stringResource(R.string.delete_download_desc)) },
                confirmButton = {
                    TextButton(onClick = {
                        scope.launch { downloadRepository.removeFromDownloads(downloadItem!!) }
                        showDeleteConfirm = false
                    }) {
                        Text(stringResource(R.string.delete_confirm), color = Color.Red)
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showDeleteConfirm = false }) { Text(stringResource(R.string.cancel)) }
                }
            )
        }"""

movie_dialog_replace = """        if (showDeleteConfirm && downloadItem != null) {
            AlertDialog(
                onDismissRequest = { showDeleteConfirm = false },
                title = { Text(if (downloadItem!!.isCompleted) stringResource(R.string.delete_download_title, movie.title) else "Cancel Download?") },
                text = { Text(if (downloadItem!!.isCompleted) stringResource(R.string.delete_download_desc) else "Are you sure you want to cancel the ongoing download?") },
                confirmButton = {
                    TextButton(onClick = {
                        val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                            action = "CANCEL"
                            putExtra("id", movie.id.toString())
                        }
                        context.startService(intent)
                        scope.launch { downloadRepository.removeFromDownloads(downloadItem!!) }
                        showDeleteConfirm = false
                    }) {
                        Text(if (downloadItem!!.isCompleted) stringResource(R.string.delete_confirm) else "Cancel Download", color = Color.Red)
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showDeleteConfirm = false }) { Text(stringResource(R.string.cancel)) }
                }
            )
        }"""
c = c.replace(movie_dialog_target, movie_dialog_replace)


# --- Fix Episode Download Button ---
ep_btn_target = """                        onDownloadClick = {
                            if (downloadItem?.isCompleted == true) {
                                scope.launch { downloadRepository.removeFromDownloads(downloadItem) }
                            } else if (downloadItem != null) {
                                scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
                            } else {
                                selectedEpisodeForSource = episode
                                isDownloadMode = true
                                if (com.example.extensions.ExtensionManager.installedExtensions.value.isEmpty()) {
                                    // No extensions logic - would be handled by parent, but let's just trigger sheet which handles it
                                }
                            }
                        }"""
# Wait, EpisodeItem needs to support onLongDownloadClick. Let's look at EpisodeItem signature.

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)

