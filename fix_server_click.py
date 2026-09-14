with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_server_click = """                                            .clickable {
                                                if (extractedQualities.isNotEmpty() && selectedServerForQuality == server) {
                                                    // Already selected
                                                } else {
                                                    selectedServerForQuality = server
                                                    extractedQualities = emptyList()
                                                    isExtractingQuality = true
                                                    qualityExtractionMessage = "جاري استخراج الجودات المتاحة..."
                                                    
                                                    val finalUrl = extractedServerLinks[server] ?: ""
                                                    
                                                    kotlinx.coroutines.GlobalScope.launch(kotlinx.coroutines.Dispatchers.Main) {
                                                        val qualities = com.example.utils.M3U8Parser.getQualities(finalUrl)
                                                        if (selectedServerForQuality == server) {
                                                            if (qualities.size <= 1) {
                                                                val dLink = extractedDownloadLinks[server] ?: ""
                                                                val watchUrl = if (finalUrl.contains("akamaized.net") || finalUrl.endsWith(".m3u8") || finalUrl.endsWith(".mp4")) {
                                                                    finalUrl
                                                                } else if (dLink.isNotEmpty()) {
                                                                    dLink
                                                                } else {
                                                                    finalUrl
                                                                }
                                                                onPlay(watchUrl, server, currentSiteName)
                                                            } else {
                                                                extractedQualities = qualities
                                                                isExtractingQuality = false
                                                                ServerStateStore.extractedQualities = qualities
                                                            }
                                                        }
                                                    }
                                                }
                                            }"""

new_server_click = """                                            .clickable {
                                                if (selectedServerForQuality == server) {
                                                    // Already selected
                                                } else {
                                                    selectedServerForQuality = server
                                                    isExtractingQuality = true
                                                    qualityExtractionMessage = "جاري الاتصال وقياس سرعة الإنترنت..."
                                                    
                                                    val finalUrl = extractedServerLinks[server] ?: ""
                                                    
                                                    kotlinx.coroutines.GlobalScope.launch(kotlinx.coroutines.Dispatchers.Main) {
                                                        val qualities = com.example.utils.M3U8Parser.getQualities(finalUrl)
                                                        if (selectedServerForQuality == server) {
                                                            com.example.ui.screens.player.ServerStateStore.serverQualities[server] = qualities
                                                            val bandwidth = com.example.utils.NetworkUtils.getEstimatedBandwidthKbps(context)
                                                            val bestQuality = com.example.utils.NetworkUtils.selectBestQuality(qualities, bandwidth)
                                                            
                                                            val watchUrl = if (qualities.isEmpty() || qualities.size == 1 && qualities[0].name == "Auto") {
                                                                val dLink = extractedDownloadLinks[server] ?: ""
                                                                if (finalUrl.contains("akamaized.net") || finalUrl.endsWith(".m3u8") || finalUrl.endsWith(".mp4")) {
                                                                    finalUrl
                                                                } else if (dLink.isNotEmpty()) {
                                                                    dLink
                                                                } else {
                                                                    finalUrl
                                                                }
                                                            } else {
                                                                bestQuality.url
                                                            }
                                                            
                                                            com.example.ui.screens.player.ServerStateStore.extractedQualities = qualities
                                                            isExtractingQuality = false
                                                            onPlay(watchUrl, server, currentSiteName)
                                                        }
                                                    }
                                                }
                                            }"""

if old_server_click in content:
    content = content.replace(old_server_click, new_server_click)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Updated ServerSelectionDialog.kt")
else:
    print("Could not find the old block to replace!")

