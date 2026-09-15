import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

old_button_block = """                    IconButton(
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

new_button_block = """                    IconButton(
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

if old_button_block in content:
    content = content.replace(old_button_block, new_button_block)
    with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Not found! Let's search with regex")
    
    # regex fallback
    match = re.search(r'IconButton\(\s*onClick = \{\s*if \(downloadItem\?\.isCompleted == true\).*?Modifier\.size\(50\.dp\).*?Icon\(Icons\.Default\.Download,.*?\}\n\s*\}', content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_button_block + content[match.end():]
        with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
            f.write(content)
        print("Replaced with regex successfully")
    else:
        print("Still not found")
