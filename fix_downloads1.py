import re
with open("app/src/main/java/com/example/data/model/DownloadItem.kt", "r") as f:
    content = f.read()

old_fields = """    @PrimaryKey val id: String,
    val title: String,"""
new_fields = """    @PrimaryKey val id: String,
    val mediaId: String,
    val title: String,"""
content = content.replace(old_fields, new_fields)

with open("app/src/main/java/com/example/data/model/DownloadItem.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "r") as f:
    content2 = f.read()

old_downloader = """    fun downloadVideo(context: Context, url: String, title: String) {
        try {
            // Clean title for file system
            val safeTitle = title.replace(Regex("[^a-zA-Z0-9.\\\\-]"), "_")
            
            // Check if it's HLS (.m3u8). Android DownloadManager natively supports standard files (.mp4, .mkv, .ts)
            // It will download .m3u8 as a tiny text file instead of the full video.
            // For a production streaming app, ExoPlayer DownloadService is used for m3u8, 
            // but we provide the standard system DownloadManager here for mp4 links.
            if (url.contains(".m3u8")) {
                Toast.makeText(context, "Downloading stream playlist (M3U8). Offline playback requires MP4.", Toast.LENGTH_LONG).show()
            }
            
            val extension = if (url.contains(".mp4")) ".mp4" else if (url.contains(".m3u8")) ".m3u8" else ".mp4"
            val fileName = "${safeTitle}_${System.currentTimeMillis()}$extension"
            
            val request = DownloadManager.Request(Uri.parse(url))"""

new_downloader = """    fun downloadVideo(context: Context, url: String, title: String, id: String) {
        try {
            if (url.contains(".m3u8")) {
                Toast.makeText(context, "Downloading stream playlist (M3U8). Offline playback requires MP4.", Toast.LENGTH_LONG).show()
            }
            
            val extension = ".mp4"
            val fileName = "${id}$extension"
            
            val destFile = java.io.File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "CineStream/$fileName")
            if (destFile.exists()) destFile.delete()
            
            val request = DownloadManager.Request(Uri.parse(url))"""

content2 = content2.replace(old_downloader, new_downloader)

with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "w") as f:
    f.write(content2)

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "r") as f:
    content3 = f.read()

content3 = content3.replace("onClick = { onItemClick(item.id, item.isMovie) }", "onClick = { onItemClick(item.mediaId, item.isMovie) }")

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "w") as f:
    f.write(content3)
