import re
with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Update signature
content = content.replace("isAnime: Boolean = false,\n    onDismiss: () -> Unit,", "isAnime: Boolean = false,\n    isDownloadMode: Boolean = false,\n    onDismiss: () -> Unit,")

# Update click handler for server
old_click = """                                                com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList() // clear so we fetch fresh
                                                onPlay(watchUrl, server, currentSiteName)"""

new_click = """                                                if (isDownloadMode) {
                                                    selectedServerForQuality = server
                                                    isExtractingQuality = true
                                                    qualityExtractionMessage = "جاري استخراج الجودات لـ $server..."
                                                    coroutineScope.launch {
                                                        val q = com.example.utils.M3U8Parser.getQualities(watchUrl)
                                                        extractedQualities = q
                                                        com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                                        isExtractingQuality = false
                                                    }
                                                } else {
                                                    com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList() // clear so we fetch fresh
                                                    onPlay(watchUrl, server, currentSiteName)
                                                }"""

content = content.replace(old_click, new_click)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
