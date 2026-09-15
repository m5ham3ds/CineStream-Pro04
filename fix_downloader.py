with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "r") as f:
    content = f.read()

new_request = """            val request = DownloadManager.Request(Uri.parse(url))
                .setTitle(title)
                .setDescription("Downloading Video via CinematicDownloader")
                .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                .setDestinationInExternalPublicDir(Environment.DIRECTORY_MOVIES, "CineStream/$fileName")
                .setAllowedOverMetered(true)
                .setAllowedOverRoaming(true)
                .addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
                .addRequestHeader("Referer", url)"""

content = content.replace(
    """            val request = DownloadManager.Request(Uri.parse(url))
                .setTitle(title)
                .setDescription("Downloading Video via CinematicDownloader")
                .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                .setDestinationInExternalPublicDir(Environment.DIRECTORY_MOVIES, "CineStream/$fileName")
                .setAllowedOverMetered(true)
                .setAllowedOverRoaming(true)""",
    new_request
)

with open("app/src/main/java/com/example/utils/AndroidDownloader.kt", "w") as f:
    f.write(content)
