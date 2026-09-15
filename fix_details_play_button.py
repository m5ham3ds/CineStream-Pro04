import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Fix Play button in MovieDetailsScreen
old_play_btn = """                    Button(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                onPlay(movie.title, "local_offline_file://${downloadItem.id}", null, null, movie.posterUrl)
                            } else {
                                val isReleased = (movie.releaseDate ?: "") <= java.time.LocalDate.now().toString()
                                if (!isReleased) {
                                    showNotReleasedDialog = true
                                } else {
                                    isDownloadMode = false
                                    if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                        showNoExtensionsDialog = true
                                    } else {
                                        showSourceSheet = true
                                    }
                                }
                            }
                        },"""

new_play_btn = """                    Button(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                onPlay(movie.title, "local_offline_file://${downloadItem.id}.mp4", null, null, movie.posterUrl)
                            } else {
                                val isReleased = (movie.releaseDate ?: "") <= java.time.LocalDate.now().toString()
                                if (!isReleased) {
                                    showNotReleasedDialog = true
                                } else {
                                    isDownloadMode = false
                                    if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                        showNoExtensionsDialog = true
                                    } else {
                                        showSourceSheet = true
                                    }
                                }
                            }
                        },"""
content = content.replace(old_play_btn, new_play_btn)

# Fix Download button in MovieDetailsScreen
old_dl_btn = """                    IconButton(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                showDeleteConfirm = true
                            } else if (downloadItem == null) {
                                isDownloadMode = true
                                
                                        if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                            showNoExtensionsDialog = true
                                        } else {
                                            showSourceSheet = true
                                        }
                            }
                        },
                        modifier = Modifier.size(50.dp).background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                    ) {
                        if (downloadItem?.isCompleted == true) {
                            Icon(Icons.Default.DownloadDone, contentDescription = "Downloaded", tint = Color.Green)
                        } else if (downloadItem != null) {
                            Icon(Icons.Default.Download, contentDescription = "Downloading", tint = MaterialTheme.colorScheme.primary)
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                        }
                    }"""

new_dl_btn = """                    IconButton(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                showDeleteConfirm = true
                            } else if (downloadItem != null) {
                                // Toggle pause
                                scope.launch {
                                    downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused))
                                }
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
                    ) {
                        if (downloadItem?.isCompleted == true) {
                            Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = MaterialTheme.colorScheme.primary)
                        } else if (downloadItem != null) {
                            AnimatedDownloadIcon(isPaused = downloadItem.isPaused)
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                        }
                    }"""
content = content.replace(old_dl_btn, new_dl_btn)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
