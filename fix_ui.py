with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Fix 1: Add import
import_stmt = "import androidx.compose.animation.animateContentSize\n"
if "animateContentSize" not in content[:1000]:
    content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\n" + import_stmt)

# Fix 2: Unresolved strings
content = content.replace("stringResource(R.string.no_sites_left)", '"لا يوجد مواقع أخرى"')
content = content.replace("stringResource(R.string.failed_all_sites)", '"عذراً، فشل البحث في جميع المواقع المتاحة."')
content = content.replace("stringResource(R.string.close)", '"إغلاق"')

# Fix 3: LazyColumn for Servers
old_server_click = """                                            .clickable {
                                                if (extractedQualities.isNotEmpty() && selectedServerForQuality == server) {
                                                    // Already selected
                                                } else {
                                                    selectedServerForQuality = server
                                                    extractedQualities = emptyList()
                                                    isExtractingQuality = true
                                                    qualityExtractionMessage = "جاري استخراج الجودات المتاحة..."
                                                    
                                                    val finalUrl = extractedServerLinks[server] ?: ""
                                                    currentExtension.extractQualities(
                                                        serverName = server,
                                                        videoUrl = finalUrl,
                                                        onQualitiesExtracted = { qualities ->
                                                            android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                                if (selectedServerForQuality == server) {
                                                                    if (qualities.isEmpty()) {
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
                                                    )
                                                }
                                            }"""

new_server_click = """                                            .clickable {
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
content = content.replace(old_server_click, new_server_click)

# Fix 4: quality.quality -> quality.name
content = content.replace("quality.quality", "quality.name")
content = content.replace("quality.name.contains(\"1080\")", "quality.name.contains(\"1080\")")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)

print("Fix applied successfully!")
