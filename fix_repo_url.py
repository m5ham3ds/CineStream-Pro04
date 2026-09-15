import re
with open("app/src/main/java/com/example/data/repository/DownloadRepository.kt", "r") as f:
    content = f.read()

old_code = """            // Use a sample real MP4 video to prove offline playback works
            val videoUrl = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
            
            val request = Request.Builder().url(videoUrl).build()"""

new_code = """            val parts = currentItem.quality.split("||")
            val videoUrl = if (parts.size > 1) parts[1] else "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
            
            val request = Request.Builder().url(videoUrl).build()"""

content = content.replace(old_code, new_code)
with open("app/src/main/java/com/example/data/repository/DownloadRepository.kt", "w") as f:
    f.write(content)
