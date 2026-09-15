import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

old_btn = """                    IconButton(
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
                            CircularProgressIndicator(progress = { downloadItem.progress }, color = MaterialTheme.colorScheme.primary, modifier = Modifier.size(24.dp))
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                        }
                    }"""

new_btn = """                    IconButton(
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
                    ) {
                        if (downloadItem?.isCompleted == true) {
                            Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = MaterialTheme.colorScheme.primary)
                        } else if (downloadItem != null) {
                            AnimatedDownloadIcon(isPaused = downloadItem.isPaused)
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                        }
                    }"""

if old_btn in content:
    content = content.replace(old_btn, new_btn)
    with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
        f.write(content)
    print("Replaced MovieDetailsScreen button successfully!")
else:
    print("Could not find the block to replace!")
