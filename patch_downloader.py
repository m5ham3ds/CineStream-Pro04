import re
with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "r") as f:
    c = f.read()

target = """            if (url.contains(".m3u8")) {
                Toast.makeText(context, "Downloading stream playlist (M3U8). Offline playback requires MP4.", Toast.LENGTH_LONG).show()
            }
            
            val extension = ".mp4"
            val fileName = "${id}$extension"
            
            val destFile = java.io.File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "CineStream/$fileName")
            if (destFile.exists()) destFile.delete()
            
            val request = DownloadManager.Request(Uri.parse(url))"""

replacement = """            val extension = ".mp4"
            val fileName = "${id}$extension"
            
            val destFile = java.io.File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "CineStream/$fileName")
            if (destFile.exists()) destFile.delete()

            if (url.contains(".m3u8")) {
                val intent = android.content.Intent(context, StreamDownloaderService::class.java).apply {
                    putExtra("url", url)
                    putExtra("title", title)
                    putExtra("id", id)
                }
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                    context.startForegroundService(intent)
                } else {
                    context.startService(intent)
                }
                Toast.makeText(context, "M3U8 Stream download started! Check notifications.", Toast.LENGTH_SHORT).show()
                return
            }
            
            val request = DownloadManager.Request(Uri.parse(url))"""

c = c.replace(target, replacement)
with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "w") as f:
    f.write(c)
