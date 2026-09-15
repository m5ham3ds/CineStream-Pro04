import re
with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Replace the isDownloadMode block
old_block = """                                                if (isDownloadMode) {
                                                    selectedServerForQuality = server
                                                    isExtractingQuality = true
                                                    qualityExtractionMessage = "جاري استخراج الجودات لـ $server..."
                                                    coroutineScope.launch {
                                                        val q = com.example.utils.M3U8Parser.getQualities(watchUrl)
                                                        extractedQualities = q
                                                        com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                                        isExtractingQuality = false
                                                    }
                                                }"""

new_block = """                                                if (isDownloadMode) {
                                                    if (watchUrl.contains(".mp4")) {
                                                        com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList()
                                                        onPlay(watchUrl, server, currentSiteName)
                                                    } else {
                                                        selectedServerForQuality = server
                                                        isExtractingQuality = true
                                                        qualityExtractionMessage = "جاري استخراج الجودات لـ $server..."
                                                        coroutineScope.launch {
                                                            val q = com.example.utils.M3U8Parser.getQualities(watchUrl)
                                                            extractedQualities = q
                                                            com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                                            isExtractingQuality = false
                                                        }
                                                    }
                                                }"""

content = content.replace(old_block, new_block)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
