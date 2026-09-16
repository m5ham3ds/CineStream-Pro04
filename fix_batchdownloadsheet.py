import re

with open("app/src/main/java/com/example/ui/components/BatchDownloadSheet.kt", "r") as f:
    c = f.read()

target = """                                    // Start batch download process
                                    scope.launch {
                                        val episodesToDownload = episodes.filter { selectedEpisodes.contains(it.id) }
                                        for (ep in episodesToDownload) {
                                            val sources = ProviderManager.extractVideoLinks(series.id, false, ep.id)
                                            if (sources.isNotEmpty()) {
                                                val preferredSource = sources.find { it.quality == targetQuality } ?: sources.first()
                                                downloadRepository.addToDownloads(
                                                    DownloadItem(
                                                        id = "${series.id}_${ep.id}",
                                                        mediaId = series.id.toString(),
                                                        title = "${series.title} - S${currentSeason?.seasonNumber}E${ep.episodeNumber}",
                                                        posterUrl = ep.thumbnailUrl,
                                                        isMovie = false,
                                                        quality = preferredSource.quality
                                                    )
                                                )
                                            }
                                        }
                                        Toast.makeText(context, "Batch download process finished", Toast.LENGTH_SHORT).show()
                                    }
                                    onDismiss()"""

replace = """                                    // Start batch download process in processor
                                    showQualitySelector = false"""

c = c.replace(target, replace)

# Add isProcessing state
target_state = """    var targetQuality by remember { mutableStateOf("") }"""
replace_state = """    var targetQuality by remember { mutableStateOf("") }
    var isProcessing by remember { mutableStateOf(false) }"""
c = c.replace(target_state, replace_state)

# Replace quality click action
target_click = """                                    targetQuality = quality
                                    showQualitySelector = false
                                    Toast.makeText(context, "Batch download started in background...", Toast.LENGTH_SHORT).show()
                                    
                                    // Start batch download process in processor"""
replace_click = """                                    targetQuality = quality
                                    showQualitySelector = false
                                    isProcessing = true"""
c = c.replace(target_click, replace_click)

# Display the processor if isProcessing is true
target_ui = """    ModalBottomSheet(onDismissRequest = onDismiss) {"""
replace_ui = """    if (isProcessing) {
        val episodesToDownload = episodes.filter { selectedEpisodes.contains(it.id) }
        BatchDownloadProcessor(
            series = series,
            seasonNumber = currentSeason?.seasonNumber ?: 1,
            episodes = episodesToDownload,
            targetQuality = targetQuality,
            onComplete = {
                isProcessing = false
                Toast.makeText(context, "تمت إضافة الحلقات لقائمة التنزيلات", Toast.LENGTH_SHORT).show()
                onDismiss()
            },
            onCancel = {
                isProcessing = false
            }
        )
        return
    }

    ModalBottomSheet(onDismissRequest = onDismiss) {"""

c = c.replace(target_ui, replace_ui)

with open("app/src/main/java/com/example/ui/components/BatchDownloadSheet.kt", "w") as f:
    f.write(c)
