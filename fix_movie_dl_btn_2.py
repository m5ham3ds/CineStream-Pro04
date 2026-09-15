import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Replace the onClick block
content = re.sub(
    r"""onClick = \{\s*if \(downloadItem\?\.isCompleted == true\) \{\s*showDeleteConfirm = true\s*\} else if \(downloadItem == null\) \{\s*isDownloadMode = true\s*if \(ExtensionManager\.installedExtensions\.value\.isEmpty\(\)\) \{\s*showNoExtensionsDialog = true\s*\} else \{\s*showSourceSheet = true\s*\}\s*\}\s*\},""",
    """onClick = { 
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
                        },""",
    content
)

# Replace the icon block
content = re.sub(
    r"""if \(downloadItem\?\.isCompleted == true\) \{\s*Icon\(Icons\.Default\.DownloadDone, contentDescription = "Downloaded", tint = Color\.Green\)\s*\} else if \(downloadItem != null\) \{\s*CircularProgressIndicator\(progress = \{ downloadItem\.progress \}, color = MaterialTheme\.colorScheme\.primary, modifier = Modifier\.size\(24\.dp\)\)\s*\} else \{\s*Icon\(Icons\.Default\.Download, contentDescription = "Download", tint = MaterialTheme\.colorScheme\.onBackground\)\s*\}""",
    """if (downloadItem?.isCompleted == true) {
                            Icon(Icons.Default.Check, contentDescription = "Downloaded", tint = MaterialTheme.colorScheme.primary)
                        } else if (downloadItem != null) {
                            AnimatedDownloadIcon(isPaused = downloadItem.isPaused)
                        } else {
                            Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                        }""",
    content
)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
print("Regex replace executed")
