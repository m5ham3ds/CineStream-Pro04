with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Add extractingEmbedUrl
content = content.replace("var isExtractingQuality by remember { mutableStateOf(false) }", "var isExtractingQuality by remember { mutableStateOf(false) }\n    var extractingEmbedUrl by remember { mutableStateOf<String?>(null) }")

# Update the click listener
old_click = """                                                    } else {
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

new_click = """                                                    } else {
                                                        selectedServerForQuality = server
                                                        isExtractingQuality = true
                                                        qualityExtractionMessage = "جاري استخراج الجودات لـ $server..."
                                                        if (watchUrl.contains(".m3u8") || watchUrl.contains("akamaized.net")) {
                                                            coroutineScope.launch {
                                                                val q = com.example.utils.M3U8Parser.getQualities(watchUrl)
                                                                extractedQualities = q
                                                                com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                                                isExtractingQuality = false
                                                            }
                                                        } else {
                                                            extractingEmbedUrl = watchUrl
                                                        }
                                                    }"""

content = content.replace(old_click, new_click)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
