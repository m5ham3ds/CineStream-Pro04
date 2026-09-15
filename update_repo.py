import re
with open("app/src/main/java/com/example/data/repository/DownloadRepository.kt", "r") as f:
    content = f.read()

# Let's replace the whole startRealDownload method
start_idx = content.find("private fun startRealDownload(id: String) {")
if start_idx != -1:
    # Find the end of the method by matching braces
    brace_count = 0
    end_idx = -1
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    if end_idx != -1:
        new_method = """private fun startRealDownload(id: String) {
        scope.launch {
            while (true) {
                var currentItem = downloadDao.getItemById(id) ?: return@launch
                if (currentItem.isCompleted) return@launch
                if (currentItem.isPaused) {
                    kotlinx.coroutines.delay(1000)
                    continue
                }

                val parts = currentItem.quality.split("||")
                val videoUrl = if (parts.size > 1) parts[1] else "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
                
                val dir = java.io.File(context.filesDir, "downloads")
                if (!dir.exists()) dir.mkdirs()
                val file = java.io.File(dir, "${id}.mp4")
                val downloadedLength = if (file.exists()) file.length() else 0L

                val requestBuilder = okhttp3.Request.Builder().url(videoUrl)
                if (downloadedLength > 0) {
                    requestBuilder.addHeader("Range", "bytes=$downloadedLength-")
                }
                
                try {
                    val response = client.newCall(requestBuilder.build()).execute()
                    if (!response.isSuccessful && response.code != 206 && response.code != 416) throw java.lang.Exception("Failed to download file: ${response.code}")
                    
                    if (response.code == 416) {
                        // Already fully downloaded or invalid range, let's mark complete
                        currentItem = currentItem.copy(progress = 1f, isCompleted = true)
                        downloadDao.updateItem(currentItem)
                        com.example.utils.NotificationHelper.showDownloadCompleted(context, currentItem.title)
                        return@launch
                    }
                    
                    val body = response.body ?: throw java.lang.Exception("Empty body")
                    val contentLength = body.contentLength() + downloadedLength
                    
                    val inputStream: java.io.InputStream = body.byteStream()
                    // append = true
                    val outputStream = java.io.FileOutputStream(file, true)
                    
                    val buffer = ByteArray(8 * 1024)
                    var bytesRead: Int
                    var totalBytesRead: Long = downloadedLength
                    
                    var lastUpdateTime = System.currentTimeMillis()
                    
                    var isPausedByUser = false
                    
                    inputStream.use { input ->
                        outputStream.use { output ->
                            while (true) {
                                val checkItem = downloadDao.getItemById(id)
                                if (checkItem == null) {
                                    file.delete()
                                    return@launch
                                }
                                if (checkItem.isPaused) {
                                    isPausedByUser = true
                                    break
                                }
                                
                                bytesRead = input.read(buffer)
                                if (bytesRead == -1) break
                                
                                output.write(buffer, 0, bytesRead)
                                totalBytesRead += bytesRead
                                
                                val currentTime = System.currentTimeMillis()
                                if (currentTime - lastUpdateTime > 500) {
                                    val progress = if (contentLength > 0) totalBytesRead.toFloat() / contentLength.toFloat() else 0f
                                    currentItem = checkItem.copy(
                                        progress = progress.coerceAtMost(0.99f)
                                    )
                                    downloadDao.updateItem(currentItem)
                                    lastUpdateTime = currentTime
                                }
                            }
                        }
                    }
                    
                    if (!isPausedByUser) {
                        // Done
                        currentItem = currentItem.copy(progress = 1f, isCompleted = true)
                        downloadDao.updateItem(currentItem)
                        com.example.utils.NotificationHelper.showDownloadCompleted(context, currentItem.title)
                        return@launch
                    }
                    
                } catch (e: Exception) {
                    e.printStackTrace()
                    currentItem = downloadDao.getItemById(id) ?: return@launch
                    currentItem = currentItem.copy(isPaused = true)
                    downloadDao.updateItem(currentItem)
                }
                
                kotlinx.coroutines.delay(2000)
            }
        }
    }"""
        
        content = content[:start_idx] + new_method + content[end_idx:]
        with open("app/src/main/java/com/example/data/repository/DownloadRepository.kt", "w") as f:
            f.write(content)
        print("Replaced startRealDownload")
    else:
        print("End of method not found")
else:
    print("Method not found")
