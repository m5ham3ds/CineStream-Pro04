with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "r") as f:
    c = f.read()

target = """    fun downloadVideo(context: Context, url: String, fileName: String, mediaId: String): Long {
        return try {
            val id = fileName.replace(".mp4", "").replace("CineStream/", "")
            val title = fileName.replace(".mp4", "")"""

replace = """    fun downloadVideo(context: Context, url: String, id: String, title: String): Long {
        return try {"""

c = c.replace(target, replace)

with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "w") as f:
    f.write(c)

