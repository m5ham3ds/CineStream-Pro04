import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

target = """                }
            }
        }
    }
}

@Composable
fun StatusBadge"""

replacement = """                }
            }
        }
        
        extractingEmbedUrl?.let { url ->
            Box(modifier = Modifier.size(1.dp).alpha(0f)) {
                com.example.ui.screens.player.HiddenVideoExtractor(
                    url = url,
                    isMovie = isMovie,
                    season = season,
                    episode = episode,
                    targetServer = selectedServerForQuality,
                    targetServerId = if (selectedServerForQuality != null) extractedServerIds[selectedServerForQuality] else null,
                    website = currentSiteName,
                    title = title,
                    onVideoUrlFound = { extractedUrl ->
                        coroutineScope.launch {
                            val q = com.example.utils.M3U8Parser.getQualities(extractedUrl)
                            if (q.isNotEmpty()) {
                                extractedQualities = q
                                com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                isExtractingQuality = false
                            } else {
                                // Direct MP4 or unknown
                                extractedQualities = listOf(com.example.utils.M3U8Parser.QualityInfo("Default", extractedUrl))
                                com.example.ui.screens.player.ServerStateStore.extractedQualities = extractedQualities
                                isExtractingQuality = false
                            }
                            extractingEmbedUrl = null
                        }
                    },
                    onIframeUrlFound = { iframeUrl ->
                        extractingEmbedUrl = iframeUrl
                    },
                    onExtractionFailed = {
                        isExtractingQuality = false
                        extractingEmbedUrl = null
                        qualityExtractionMessage = "فشل استخراج الجودات"
                    }
                )
            }
        }
    }
}

@Composable
fun StatusBadge"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
