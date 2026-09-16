with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

target = """                }
            }
        }
    }
}

@Composable"""

replacement = """                }
            }
            
            if (extractingEmbedUrl != null) {
                Box(modifier = Modifier.size(0.dp).alpha(0f)) {
                    com.example.ui.screens.player.HiddenVideoExtractor(
                        url = extractingEmbedUrl!!,
                        isMovie = isMovie,
                        season = season,
                        episode = episode,
                        targetServer = selectedServerForQuality,
                        website = currentSiteName,
                        title = title,
                        onVideoUrlFound = { foundUrl ->
                            extractingEmbedUrl = null
                            if (foundUrl.isNotEmpty()) {
                                if (foundUrl.contains(".mp4") && !foundUrl.contains(".m3u8")) {
                                    // It's a direct mp4, skip quality extraction
                                    com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList()
                                    isExtractingQuality = false
                                    onPlay(foundUrl, selectedServerForQuality ?: "", currentSiteName)
                                } else {
                                    coroutineScope.launch {
                                        val q = com.example.utils.M3U8Parser.getQualities(foundUrl)
                                        extractedQualities = q
                                        com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                        isExtractingQuality = false
                                    }
                                }
                            } else {
                                isExtractingQuality = false
                            }
                        }
                    )
                }
            }
        }
    }
}

@Composable"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
