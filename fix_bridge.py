import re

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "r") as f:
    c = f.read()

target = """                            onServersExtracted = { serversNames, serversMap, downloadsMap, serversIds ->
                                android.os.Handler(android.os.Looper.getMainLooper()).post {
                                    val firstServer = serversNames.firstOrNull()
                                    if (firstServer != null) {
                                        val finalUrl = serversMap[firstServer] ?: ""
                                        val dLink = downloadsMap[firstServer] ?: ""
                                        val watchUrl = if (finalUrl.contains("akamaized.net") || finalUrl.endsWith(".m3u8") || finalUrl.endsWith(".mp4")) {
                                            finalUrl
                                        } else if (dLink.isNotEmpty()) {
                                            dLink
                                        } else {
                                            finalUrl
                                        }
                                        
                                        if (watchUrl.contains(".mp4")) {
                                            // Direct MP4
                                            scope.launch {
                                                val fullTitle = "${series.title} - S${seasonNumber}E${episode.episodeNumber}"
                                                val epIdStr = "${series.id}_${episode.id}"
                                                downloadRepository.addToDownloads(DownloadItem(
                                                    id = epIdStr, mediaId = series.id.toString(), title = fullTitle, posterUrl = episode.thumbnailUrl, isMovie = false, quality = "$firstServer||$watchUrl"
                                                ))
                                                com.example.utils.AndroidDownloader.downloadVideo(context, watchUrl, epIdStr, "$fullTitle - $firstServer")
                                                currentIndex++
                                                phase = "INIT"
                                            }
                                        } else {
                                            currentEmbedUrl = watchUrl
                                            phase = "EXTRACTING_URL"
                                        }
                                    } else {
                                        // No servers found, skip episode
                                        currentIndex++
                                        phase = "INIT"
                                    }
                                }
                            }"""

replace = """                            onSendFailed = {
                                android.os.Handler(android.os.Looper.getMainLooper()).post {
                                    currentIndex++
                                    phase = "INIT"
                                }
                            },
                            onSendServers = { _, _ -> },
                            onSendServersV2 = { serversJson, _ ->
                                android.os.Handler(android.os.Looper.getMainLooper()).post {
                                    try {
                                        val serversData = org.json.JSONArray(serversJson)
                                        val serversNames = mutableListOf<String>()
                                        val serversMap = mutableMapOf<String, String>()
                                        val downloadsMap = mutableMapOf<String, String>()
                                        
                                        for (i in 0 until serversData.length()) {
                                            val item = serversData.getJSONObject(i)
                                            val name = item.getString("name")
                                            val link = if (item.has("link")) item.getString("link") else if (item.has("url")) item.getString("url") else ""
                                            if (name.contains("(تحميل)") || link.endsWith(".mp4") || link.endsWith(".mkv")) {
                                                downloadsMap[name] = link
                                            } else {
                                                serversNames.add(name)
                                                serversMap[name] = link
                                            }
                                        }
                                        
                                        val firstServer = serversNames.firstOrNull()
                                        if (firstServer != null) {
                                            val finalUrl = serversMap[firstServer] ?: ""
                                            val dLink = downloadsMap[firstServer] ?: ""
                                            val watchUrl = if (finalUrl.contains("akamaized.net") || finalUrl.endsWith(".m3u8") || finalUrl.endsWith(".mp4")) {
                                                finalUrl
                                            } else if (dLink.isNotEmpty()) {
                                                dLink
                                            } else {
                                                finalUrl
                                            }
                                            
                                            if (watchUrl.contains(".mp4") && !watchUrl.contains(".m3u8")) {
                                                scope.launch {
                                                    val rawTitle = series.originalTitle ?: series.title
                                                    val fullTitle = "$rawTitle - S${seasonNumber}E${episode.episodeNumber}"
                                                    val epIdStr = "${series.id}_${episode.id}"
                                                    downloadRepository.addToDownloads(DownloadItem(
                                                        id = epIdStr, mediaId = series.id.toString(), title = fullTitle, posterUrl = episode.thumbnailUrl, isMovie = false, quality = "$firstServer||$watchUrl"
                                                    ))
                                                    com.example.utils.AndroidDownloader.downloadVideo(context, watchUrl, epIdStr, "$fullTitle - $firstServer")
                                                    currentIndex++
                                                    phase = "INIT"
                                                }
                                            } else {
                                                currentEmbedUrl = watchUrl
                                                phase = "EXTRACTING_URL"
                                            }
                                        } else {
                                            currentIndex++
                                            phase = "INIT"
                                        }
                                    } catch (e: Exception) {
                                        currentIndex++
                                        phase = "INIT"
                                    }
                                }
                            }"""

c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "w") as f:
    f.write(c)
