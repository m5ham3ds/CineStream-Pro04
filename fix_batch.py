import re
with open("app/src/main/java/com/example/ui/components/BatchDownloadSheet.kt", "r") as f:
    content = f.read()

old_dl = """                                                downloadRepository.addToDownloads(
                                                    DownloadItem(
                                                        id = ep.id,
                                                        title = "${series.title} - S${currentSeason?.seasonNumber}E${ep.episodeNumber}",
                                                        posterUrl = ep.thumbnailUrl,
                                                        isMovie = false,
                                                        quality = preferredSource.quality
                                                    )
                                                )
                                                com.example.utils.AndroidDownloader.downloadVideo(context, preferredSource.url, "${series.title} - S${currentSeason?.seasonNumber}E${ep.episodeNumber} - ${preferredSource.quality}")"""

new_dl = """                                                val epIdStr = "${series.id}_${ep.id}"
                                                downloadRepository.addToDownloads(
                                                    DownloadItem(
                                                        id = epIdStr,
                                                        mediaId = series.id.toString(),
                                                        title = "${series.title} - S${currentSeason?.seasonNumber}E${ep.episodeNumber}",
                                                        posterUrl = ep.thumbnailUrl,
                                                        isMovie = false,
                                                        quality = preferredSource.quality
                                                    )
                                                )
                                                com.example.utils.AndroidDownloader.downloadVideo(context, preferredSource.url, "${series.title} - S${currentSeason?.seasonNumber}E${ep.episodeNumber} - ${preferredSource.quality}", epIdStr)"""

content = content.replace(old_dl, new_dl)

with open("app/src/main/java/com/example/ui/components/BatchDownloadSheet.kt", "w") as f:
    f.write(content)
