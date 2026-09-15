import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

old_click = """                            onClick = {
                                selectedEpisodeForSource = episode
                                isDownloadMode = false
                            },"""
new_click = """                            onClick = {
                                if (isDownloaded) {
                                    scope.launch {
                                        val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${episode.episodeNumber}"
                                        historyRepository.addToHistory(
                                            com.example.data.model.HistoryItem(
                                                id = series.id.toString(), title = fullTitle, posterUrl = episode.thumbnailUrl, isMovie = false
                                            )
                                        )
                                        onPlay(fullTitle, "local_offline_file://${series.id}_${episode.id}", null, null)
                                    }
                                } else {
                                    selectedEpisodeForSource = episode
                                    isDownloadMode = false
                                }
                            },"""

content = content.replace(old_click, new_click)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
