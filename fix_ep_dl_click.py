import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

old_click = """                            onDownloadClick = {
                                selectedEpisodeForSource = episode
                                isDownloadMode = true
                            }"""

new_click = """                            onDownloadClick = {
                                if (downloadItem?.isCompleted == true) {
                                    scope.launch { downloadRepository.removeFromDownloads(downloadItem) }
                                } else if (downloadItem != null) {
                                    scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
                                } else {
                                    selectedEpisodeForSource = episode
                                    isDownloadMode = true
                                    if (com.example.data.extension.ExtensionManager.installedExtensions.value.isEmpty()) {
                                        // No extensions logic - would be handled by parent, but let's just trigger sheet which handles it
                                    }
                                }
                            }"""

content = content.replace(old_click, new_click)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
